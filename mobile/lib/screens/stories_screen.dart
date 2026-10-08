import 'package:flutter/material.dart';
import '../data/app_database.dart';

class StoriesScreen extends StatelessWidget {
  final AppDatabase db;
  const StoriesScreen({super.key, required this.db});

  @override
  Widget build(BuildContext context) {
    return Directionality(
      textDirection: TextDirection.rtl,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text('📖 عالم القصص', style: Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height: 12),
          ...List.generate(
            13,
            (i) => Card(
              child: ListTile(
                leading: CircleAvatar(child: Text(i.toString())),
                title: Text('قصة المستوى ' + i.toString()),
                subtitle: const Text('استمع، اقرأ، أجب، ثم أعد سرد القصة.'),
                onTap: () => showDialog(
                  context: context,
                  builder: (_) => AlertDialog(
                    title: Text('قصة المستوى ' + i.toString()),
                    content: const Text('المحتوى المحلي مصمم ليعمل دون اتصال ويمكن توسيعه بوسائط أصلية ومرخّصة.'),
                    actions: [
                      TextButton(onPressed: () => Navigator.pop(context), child: const Text('إغلاق')),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
