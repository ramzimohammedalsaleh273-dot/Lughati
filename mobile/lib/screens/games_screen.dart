import 'dart:math';
import 'package:flutter/material.dart';
import '../data/app_database.dart';

class GamesScreen extends StatefulWidget {
  final AppDatabase db;
  const GamesScreen({super.key, required this.db});
  @override State<GamesScreen> createState() => _GamesState();
}

class _GamesState extends State<GamesScreen> {
  String lang = 'ar';
  Map<String, dynamic>? word;
  int score = 0;
  final Random random = Random();

  @override
  void initState() { super.initState(); _newWord(); }

  Future<void> _newWord() async {
    final list = await widget.db.words(lang);
    if (list.isNotEmpty && mounted) setState(() => word = list[random.nextInt(list.length)]);
  }

  @override
  Widget build(BuildContext context) {
    return Directionality(
      textDirection: TextDirection.rtl,
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            Text('🎮 تحدي المفردات', style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 20),
            if (word != null)
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: Column(
                    children: [
                      Text(word!['text'].toString(), style: const TextStyle(fontSize: 40, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 10),
                      Text(word!['example'].toString()),
                      const SizedBox(height: 20),
                      FilledButton(
                        onPressed: () { setState(() => score++); _newWord(); },
                        child: const Text('عرفتها ✓'),
                      ),
                      OutlinedButton(onPressed: _newWord, child: const Text('كلمة أخرى')),
                    ],
                  ),
                ),
              ),
            const SizedBox(height: 12),
            Text('النقاط: ' + score.toString()),
          ],
        ),
      ),
    );
  }
}
