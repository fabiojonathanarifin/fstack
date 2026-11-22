import { View, Text, StyleSheet } from 'react-native';

export default function Card({ title, body }) {
  return (
    <View style={styles.card}>
      <Text style={styles.title}>{title}</Text>
      <Text>{body}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: { padding: 16, borderRadius: 12, backgroundColor: '#fff' },
  title: { fontWeight: '600', marginBottom: 8 },
});
