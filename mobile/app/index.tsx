import { View, Text, TouchableOpacity, StyleSheet, ScrollView, Dimensions } from 'react-native'
import { useRouter } from 'expo-router'
import { StatusBar } from 'expo-status-bar'
import { SafeAreaView } from 'react-native-safe-area-context'
import { Ionicons } from '@expo/vector-icons'

const { width } = Dimensions.get('window')

const FEATURES = [
  { icon: 'people-outline', title: 'Smart HR Connect', desc: 'Auto-connects with HRs and hiring managers who can actually get you hired.' },
  { icon: 'mail-outline', title: 'Cold Email Engine', desc: 'Finds valid HR emails and sends personalized cold emails directly.' },
  { icon: 'document-text-outline', title: 'ATS-Semantic Engine', desc: 'NLP-powered resume optimization. Passes every ATS filter.' },
  { icon: 'map-outline', title: 'Career Roadmap', desc: 'Skill gap analysis and "what to do next" with real course links.' },
  { icon: 'shield-checkmark-outline', title: 'Human-in-the-Loop', desc: 'You review every message before it goes out. Full control.' },
  { icon: 'flash-outline', title: 'LinkedIn Autopilot', desc: 'Posts, connections, messages — all automated safely.' },
]

export default function LandingScreen() {
  const router = useRouter()

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="light" />
      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.scroll}>

        {/* Nav */}
        <View style={styles.nav}>
          <AscendraLogo />
          <TouchableOpacity style={styles.navBtn} onPress={() => router.push('/chat')}>
            <Text style={styles.navBtnText}>Open App</Text>
            <Ionicons name="arrow-forward" size={14} color="#fff" />
          </TouchableOpacity>
        </View>

        {/* Hero */}
        <View style={styles.hero}>
          <View style={styles.badge}>
            <Ionicons name="star" size={11} color="#d4891e" />
            <Text style={styles.badgeText}>AI Career Intelligence Platform</Text>
          </View>

          <Text style={styles.heroTitle}>
            Land Your{'\n'}
            <Text style={styles.heroTitleGold}>Dream Job.</Text>
          </Text>

          <Text style={styles.heroSub}>
            Ascendra is your autonomous AI career co-pilot. Connect with HRs, send cold messages,
            build ATS-optimized resumes — all from a single chat.
          </Text>

          <TouchableOpacity style={styles.ctaPrimary} onPress={() => router.push('/chat')} activeOpacity={0.85}>
            <Text style={styles.ctaPrimaryText}>Start for Free</Text>
            <Ionicons name="arrow-forward" size={16} color="#fff" />
          </TouchableOpacity>
        </View>

        {/* Features */}
        <View style={styles.featuresSection}>
          <Text style={styles.sectionTitle}>Everything to <Text style={styles.sectionTitleGold}>Rise</Text></Text>
          <Text style={styles.sectionSub}>One AI. Complete career automation.</Text>

          <View style={styles.featuresGrid}>
            {FEATURES.map(({ icon, title, desc }) => (
              <View key={title} style={styles.featureCard}>
                <View style={styles.featureIcon}>
                  <Ionicons name={icon as any} size={20} color="#d4891e" />
                </View>
                <Text style={styles.featureTitle}>{title}</Text>
                <Text style={styles.featureDesc}>{desc}</Text>
              </View>
            ))}
          </View>
        </View>

        {/* CTA */}
        <View style={styles.ctaSection}>
          <View style={styles.ctaCard}>
            <Text style={styles.ctaTitle}>Ready to{'\n'}<Text style={styles.ctaTitleGold}>Ascend?</Text></Text>
            <Text style={styles.ctaSub}>Your dream job is one conversation away.</Text>
            <TouchableOpacity style={styles.ctaPrimary} onPress={() => router.push('/chat')} activeOpacity={0.85}>
              <Text style={styles.ctaPrimaryText}>Launch Ascendra</Text>
              <Ionicons name="arrow-forward" size={16} color="#fff" />
            </TouchableOpacity>
          </View>
        </View>

        {/* Footer */}
        <View style={styles.footer}>
          <AscendraLogo small />
          <Text style={styles.footerText}>© 2026 Ascendra · Rise Without Limits · Personal use only</Text>
        </View>

      </ScrollView>
    </SafeAreaView>
  )
}

function AscendraLogo({ small = false }: { small?: boolean }) {
  return (
    <View style={[styles.logoRow, small && { transform: [{ scale: 0.85 }] }]}>
      <View style={styles.logoIcon}>
        <Ionicons name="trending-up" size={14} color="#d4891e" />
      </View>
      <Text style={styles.logoText}>Ascendra</Text>
    </View>
  )
}

const GOLD = '#d4891e'
const BG0 = '#080810'
const BG2 = '#121220'
const BG3 = '#181828'

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: BG0 },
  scroll: { paddingBottom: 40 },

  nav: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: 20, paddingVertical: 14 },
  navBtn: { flexDirection: 'row', alignItems: 'center', gap: 6, backgroundColor: GOLD, paddingHorizontal: 16, paddingVertical: 8, borderRadius: 20 },
  navBtnText: { color: '#fff', fontSize: 13, fontWeight: '600' },

  hero: { paddingHorizontal: 24, paddingTop: 32, paddingBottom: 48, alignItems: 'flex-start' },
  badge: { flexDirection: 'row', alignItems: 'center', gap: 6, paddingHorizontal: 12, paddingVertical: 6, borderRadius: 20, borderWidth: 1, borderColor: 'rgba(212,137,30,0.3)', backgroundColor: 'rgba(212,137,30,0.08)', marginBottom: 24 },
  badgeText: { color: '#e3a33a', fontSize: 12, fontWeight: '500' },
  heroTitle: { fontSize: 44, fontWeight: '800', color: '#fff', lineHeight: 48, marginBottom: 16, letterSpacing: -1 },
  heroTitleGold: { color: GOLD },
  heroSub: { fontSize: 16, color: 'rgba(255,255,255,0.45)', lineHeight: 24, marginBottom: 32, fontWeight: '300' },

  ctaPrimary: { flexDirection: 'row', alignItems: 'center', gap: 8, backgroundColor: GOLD, paddingHorizontal: 28, paddingVertical: 14, borderRadius: 16 },
  ctaPrimaryText: { color: '#fff', fontSize: 15, fontWeight: '700' },

  featuresSection: { paddingHorizontal: 20, paddingBottom: 40 },
  sectionTitle: { fontSize: 28, fontWeight: '800', color: '#fff', textAlign: 'center', marginBottom: 8, letterSpacing: -0.5 },
  sectionTitleGold: { color: GOLD },
  sectionSub: { fontSize: 14, color: 'rgba(255,255,255,0.4)', textAlign: 'center', marginBottom: 24 },
  featuresGrid: { gap: 12 },
  featureCard: { backgroundColor: BG2, borderWidth: 1, borderColor: 'rgba(255,255,255,0.06)', borderRadius: 16, padding: 18 },
  featureIcon: { width: 40, height: 40, borderRadius: 12, backgroundColor: 'rgba(212,137,30,0.12)', borderWidth: 1, borderColor: 'rgba(212,137,30,0.2)', alignItems: 'center', justifyContent: 'center', marginBottom: 12 },
  featureTitle: { color: '#fff', fontSize: 14, fontWeight: '700', marginBottom: 4 },
  featureDesc: { color: 'rgba(255,255,255,0.4)', fontSize: 13, lineHeight: 19 },

  ctaSection: { paddingHorizontal: 20, marginBottom: 32 },
  ctaCard: { backgroundColor: BG3, borderWidth: 1, borderColor: 'rgba(212,137,30,0.2)', borderRadius: 24, padding: 32, alignItems: 'center' },
  ctaTitle: { fontSize: 36, fontWeight: '800', color: '#fff', textAlign: 'center', marginBottom: 12, letterSpacing: -0.5 },
  ctaTitleGold: { color: GOLD },
  ctaSub: { color: 'rgba(255,255,255,0.4)', fontSize: 15, textAlign: 'center', marginBottom: 28 },

  footer: { paddingHorizontal: 20, paddingTop: 20, borderTopWidth: 1, borderTopColor: 'rgba(255,255,255,0.05)', alignItems: 'center', gap: 8 },
  footerText: { color: 'rgba(255,255,255,0.2)', fontSize: 11, textAlign: 'center' },

  logoRow: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  logoIcon: { width: 28, height: 28, borderRadius: 8, backgroundColor: 'rgba(212,137,30,0.15)', borderWidth: 1, borderColor: 'rgba(212,137,30,0.3)', alignItems: 'center', justifyContent: 'center' },
  logoText: { color: '#fff', fontSize: 16, fontWeight: '700', letterSpacing: -0.3 },
})
