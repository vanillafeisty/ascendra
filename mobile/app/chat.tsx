import { useState, useRef, useCallback, useEffect } from 'react'
import {
  View, Text, TextInput, TouchableOpacity, FlatList,
  StyleSheet, KeyboardAvoidingView, Platform, ActivityIndicator,
  Animated, Vibration
} from 'react-native'
import { SafeAreaView, useSafeAreaInsets } from 'react-native-safe-area-context'
import { useRouter } from 'expo-router'
import { Ionicons } from '@expo/vector-icons'
import AsyncStorage from '@react-native-async-storage/async-storage'
import * as Clipboard from 'expo-clipboard'
import * as Haptics from 'expo-haptics'
import Markdown from 'react-native-markdown-display'
import { moderateContent } from '../src/lib/moderation'
import { STARTER_PROMPTS, BACKEND_URL } from '../src/lib/constants'
import type { Message } from '../src/lib/types'

export default function ChatScreen() {
  const router = useRouter()
  const insets = useSafeAreaInsets()
  const flatListRef = useRef<FlatList>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [copiedId, setCopiedId] = useState<string | null>(null)

  // Load persisted messages
  useEffect(() => {
    AsyncStorage.getItem('ascendra_messages').then(data => {
      if (data) setMessages(JSON.parse(data))
    })
  }, [])

  // Persist messages
  useEffect(() => {
    if (messages.length > 0) {
      AsyncStorage.setItem('ascendra_messages', JSON.stringify(messages.slice(-100)))
    }
  }, [messages])

  async function sendMessage() {
    const text = input.trim()
    if (!text || isLoading) return

    // Content moderation check
    const mod = moderateContent(text)
    if (mod.blocked) {
      await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Warning)
      const blockedMsg: Message = { id: Date.now().toString(), role: 'assistant', content: mod.response! }
      setMessages(prev => [...prev, { id: (Date.now() - 1).toString(), role: 'user', content: text }, blockedMsg])
      setInput('')
      return
    }

    await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light)

    const userMsg: Message = { id: Date.now().toString(), role: 'user', content: text }
    const newMessages = [...messages, userMsg]
    setMessages(newMessages)
    setInput('')
    setIsLoading(true)

    try {
      const response = await fetch(`${BACKEND_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: newMessages.map(m => ({ role: m.role, content: m.content }))
        }),
      })

      if (!response.ok) throw new Error('API error')
      const data = await response.json()

      const assistantMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.message || data.content || 'Something went wrong. Please try again.'
      }
      setMessages(prev => [...prev, assistantMsg])
      await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light)
    } catch (err) {
      const errMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `⚠️ Unable to reach Ascendra backend. Make sure \`api.py\` is running at ${BACKEND_URL}.\n\nFor web use, you get full streaming — the mobile app connects to the same backend.`
      }
      setMessages(prev => [...prev, errMsg])
    } finally {
      setIsLoading(false)
      setTimeout(() => flatListRef.current?.scrollToEnd({ animated: true }), 100)
    }
  }

  async function copyMessage(content: string, id: string) {
    await Clipboard.setStringAsync(content)
    await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 1500)
  }

  function clearChat() {
    setMessages([])
    AsyncStorage.removeItem('ascendra_messages')
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium)
  }

  const renderMessage = useCallback(({ item }: { item: Message }) => {
    const isUser = item.role === 'user'
    return (
      <View style={[styles.msgRow, isUser && styles.msgRowUser]}>
        {!isUser && (
          <View style={styles.avatar}>
            <Ionicons name="flash" size={12} color="#d4891e" />
          </View>
        )}
        <View style={[styles.bubble, isUser ? styles.bubbleUser : styles.bubbleAI]}>
          {isUser ? (
            <Text style={styles.bubbleUserText}>{item.content}</Text>
          ) : (
            <>
              <Text style={styles.aiLabel}>ASCENDRA</Text>
              <Markdown style={markdownStyles}>{item.content}</Markdown>
              <TouchableOpacity style={styles.copyBtn} onPress={() => copyMessage(item.content, item.id)}>
                <Ionicons name={copiedId === item.id ? 'checkmark' : 'copy-outline'} size={12} color="rgba(255,255,255,0.3)" />
                <Text style={styles.copyText}>{copiedId === item.id ? 'Copied' : 'Copy'}</Text>
              </TouchableOpacity>
            </>
          )}
        </View>
      </View>
    )
  }, [copiedId])

  const isEmpty = messages.length === 0

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.headerBtn}>
          <Ionicons name="chevron-back" size={20} color="rgba(255,255,255,0.5)" />
        </TouchableOpacity>
        <View style={styles.headerCenter}>
          <View style={styles.headerLogo}>
            <Ionicons name="trending-up" size={12} color="#d4891e" />
          </View>
          <Text style={styles.headerTitle}>Ascendra</Text>
          <View style={styles.onlineDot} />
        </View>
        <TouchableOpacity onPress={clearChat} style={styles.headerBtn}>
          <Ionicons name="create-outline" size={18} color="rgba(255,255,255,0.5)" />
        </TouchableOpacity>
      </View>

      {/* Messages / Welcome */}
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 20}
      >
        {isEmpty ? (
          <WelcomeView onPrompt={p => { setInput(p) }} />
        ) : (
          <FlatList
            ref={flatListRef}
            data={messages}
            keyExtractor={m => m.id}
            renderItem={renderMessage}
            contentContainerStyle={styles.messagesList}
            onContentSizeChange={() => flatListRef.current?.scrollToEnd({ animated: false })}
            showsVerticalScrollIndicator={false}
            ListFooterComponent={isLoading ? <ThinkingBubble /> : null}
          />
        )}

        {/* Input bar */}
        <View style={[styles.inputBar, { paddingBottom: insets.bottom + 8 }]}>
          <View style={styles.inputWrap}>
            <TextInput
              style={styles.textInput}
              value={input}
              onChangeText={setInput}
              placeholder="Ask Ascendra anything…"
              placeholderTextColor="rgba(255,255,255,0.2)"
              multiline
              maxLength={2000}
              returnKeyType="send"
              onSubmitEditing={sendMessage}
              editable={!isLoading}
            />
            <TouchableOpacity
              style={[styles.sendBtn, (!input.trim() || isLoading) && styles.sendBtnDisabled]}
              onPress={sendMessage}
              disabled={!input.trim() || isLoading}
              activeOpacity={0.8}
            >
              {isLoading
                ? <ActivityIndicator size="small" color="#fff" />
                : <Ionicons name="arrow-up" size={16} color="#fff" />
              }
            </TouchableOpacity>
          </View>
          <Text style={styles.disclaimer}>Review all automated actions before sending · Personal use only</Text>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  )
}

function WelcomeView({ onPrompt }: { onPrompt: (p: string) => void }) {
  return (
    <FlatList
      data={STARTER_PROMPTS}
      keyExtractor={i => i.title}
      numColumns={2}
      showsVerticalScrollIndicator={false}
      contentContainerStyle={styles.welcomeContainer}
      ListHeaderComponent={
        <View style={styles.welcomeHeader}>
          <View style={styles.welcomeAvatarBig}>
            <Ionicons name="flash" size={28} color="#d4891e" />
          </View>
          <Text style={styles.welcomeTitle}>How can I help you{'\n'}<Text style={{ color: '#d4891e' }}>rise today?</Text></Text>
          <Text style={styles.welcomeSub}>Tell me your goal — I'll handle everything else.</Text>
        </View>
      }
      renderItem={({ item }) => (
        <TouchableOpacity style={styles.starterCard} onPress={() => onPrompt(item.prompt)} activeOpacity={0.75}>
          <Text style={styles.starterEmoji}>{item.icon}</Text>
          <Text style={styles.starterTitle}>{item.title}</Text>
          <Text style={styles.starterDesc} numberOfLines={2}>{item.prompt.slice(0, 65)}…</Text>
        </TouchableOpacity>
      )}
      columnWrapperStyle={{ gap: 10 }}
    />
  )
}

function ThinkingBubble() {
  return (
    <View style={styles.msgRow}>
      <View style={styles.avatar}>
        <Ionicons name="flash" size={12} color="#d4891e" />
      </View>
      <View style={[styles.bubble, styles.bubbleAI, { paddingVertical: 12, paddingHorizontal: 16 }]}>
        <View style={{ flexDirection: 'row', gap: 5, alignItems: 'center' }}>
          {[0, 1, 2].map(i => (
            <View key={i} style={[styles.dot, { opacity: 0.6 }]} />
          ))}
        </View>
      </View>
    </View>
  )
}

const GOLD = '#d4891e'
const BG0 = '#080810'
const BG2 = '#121220'
const BG3 = '#181828'
const BG4 = '#1e1e30'

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: BG0 },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: 12, height: 52, borderBottomWidth: 1, borderBottomColor: 'rgba(255,255,255,0.05)' },
  headerBtn: { width: 36, height: 36, alignItems: 'center', justifyContent: 'center', borderRadius: 10 },
  headerCenter: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  headerLogo: { width: 26, height: 26, borderRadius: 8, backgroundColor: 'rgba(212,137,30,0.15)', borderWidth: 1, borderColor: 'rgba(212,137,30,0.3)', alignItems: 'center', justifyContent: 'center' },
  headerTitle: { color: '#fff', fontSize: 15, fontWeight: '700' },
  onlineDot: { width: 6, height: 6, borderRadius: 3, backgroundColor: '#22c55e' },

  messagesList: { paddingHorizontal: 16, paddingVertical: 12, paddingBottom: 8 },
  msgRow: { flexDirection: 'row', alignItems: 'flex-start', marginBottom: 12, gap: 8 },
  msgRowUser: { justifyContent: 'flex-end' },
  avatar: { width: 30, height: 30, borderRadius: 10, backgroundColor: 'rgba(212,137,30,0.12)', borderWidth: 1, borderColor: 'rgba(212,137,30,0.25)', alignItems: 'center', justifyContent: 'center', marginTop: 2, flexShrink: 0 },
  bubble: { borderRadius: 16, maxWidth: '82%', padding: 14 },
  bubbleUser: { backgroundColor: 'rgba(212,137,30,0.12)', borderWidth: 1, borderColor: 'rgba(212,137,30,0.2)', borderTopRightRadius: 4 },
  bubbleAI: { backgroundColor: BG3, borderWidth: 1, borderColor: 'rgba(255,255,255,0.06)', borderTopLeftRadius: 4, flex: 1 },
  bubbleUserText: { color: 'rgba(255,255,255,0.9)', fontSize: 14, lineHeight: 20 },
  aiLabel: { color: 'rgba(212,137,30,0.6)', fontSize: 9, fontWeight: '700', letterSpacing: 1.5, marginBottom: 6 },
  copyBtn: { flexDirection: 'row', alignItems: 'center', gap: 4, marginTop: 8 },
  copyText: { color: 'rgba(255,255,255,0.25)', fontSize: 11 },
  dot: { width: 6, height: 6, borderRadius: 3, backgroundColor: GOLD },

  inputBar: { paddingHorizontal: 14, paddingTop: 10, borderTopWidth: 1, borderTopColor: 'rgba(255,255,255,0.05)', backgroundColor: BG0 },
  inputWrap: { flexDirection: 'row', alignItems: 'flex-end', gap: 10, backgroundColor: BG3, borderWidth: 1, borderColor: 'rgba(255,255,255,0.08)', borderRadius: 20, paddingHorizontal: 16, paddingVertical: 10 },
  textInput: { flex: 1, color: '#fff', fontSize: 14, lineHeight: 20, maxHeight: 120, paddingTop: 0 },
  sendBtn: { width: 34, height: 34, borderRadius: 17, backgroundColor: GOLD, alignItems: 'center', justifyContent: 'center', flexShrink: 0 },
  sendBtnDisabled: { opacity: 0.3 },
  disclaimer: { color: 'rgba(255,255,255,0.15)', fontSize: 10, textAlign: 'center', marginTop: 6 },

  welcomeContainer: { paddingHorizontal: 16, paddingVertical: 20, paddingBottom: 16 },
  welcomeHeader: { alignItems: 'center', paddingBottom: 28 },
  welcomeAvatarBig: { width: 64, height: 64, borderRadius: 20, backgroundColor: 'rgba(212,137,30,0.12)', borderWidth: 1, borderColor: 'rgba(212,137,30,0.3)', alignItems: 'center', justifyContent: 'center', marginBottom: 20 },
  welcomeTitle: { color: '#fff', fontSize: 28, fontWeight: '800', textAlign: 'center', lineHeight: 36, marginBottom: 10, letterSpacing: -0.5 },
  welcomeSub: { color: 'rgba(255,255,255,0.35)', fontSize: 14, textAlign: 'center' },
  starterCard: { flex: 1, backgroundColor: BG2, borderWidth: 1, borderColor: 'rgba(255,255,255,0.06)', borderRadius: 16, padding: 14, marginBottom: 10 },
  starterEmoji: { fontSize: 22, marginBottom: 8 },
  starterTitle: { color: 'rgba(255,255,255,0.8)', fontSize: 13, fontWeight: '700', marginBottom: 4 },
  starterDesc: { color: 'rgba(255,255,255,0.3)', fontSize: 11, lineHeight: 16 },
})

const markdownStyles = StyleSheet.create({
  body: { color: 'rgba(255,255,255,0.8)', fontSize: 14, lineHeight: 21 },
  strong: { color: '#fff', fontWeight: '700' },
  em: { color: 'rgba(255,255,255,0.7)', fontStyle: 'italic' },
  code_inline: { backgroundColor: 'rgba(255,255,255,0.08)', color: '#d4891e', fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace', fontSize: 12, borderRadius: 4, paddingHorizontal: 4 },
  fence: { backgroundColor: '#0d0d1e', borderRadius: 8, padding: 12, borderWidth: 1, borderColor: 'rgba(255,255,255,0.08)' },
  code_block: { color: 'rgba(255,255,255,0.8)', fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace', fontSize: 12 },
  bullet_list_icon: { color: '#d4891e', marginTop: 3 },
  ordered_list_icon: { color: '#d4891e' },
  link: { color: '#d4891e', textDecorationLine: 'underline' },
  heading1: { color: '#fff', fontSize: 18, fontWeight: '800', marginVertical: 8 },
  heading2: { color: '#fff', fontSize: 16, fontWeight: '700', marginVertical: 6 },
  heading3: { color: '#fff', fontSize: 14, fontWeight: '700', marginVertical: 4 },
  blockquote: { borderLeftWidth: 3, borderLeftColor: 'rgba(212,137,30,0.5)', paddingLeft: 10, marginVertical: 6 },
  hr: { borderTopWidth: 1, borderTopColor: 'rgba(255,255,255,0.08)', marginVertical: 12 },
  table: { borderWidth: 1, borderColor: 'rgba(255,255,255,0.1)', borderRadius: 6, marginVertical: 8 },
  th: { backgroundColor: 'rgba(255,255,255,0.05)', padding: 8 },
  td: { padding: 8, borderTopWidth: 1, borderTopColor: 'rgba(255,255,255,0.05)' },
} as any)
