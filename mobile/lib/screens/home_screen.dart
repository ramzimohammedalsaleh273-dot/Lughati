import 'package:flutter/material.dart';
import '../data/app_database.dart';
import 'learn_screen.dart';
import 'games_screen.dart';
import 'stories_screen.dart';
import 'parent_screen.dart';
import 'media_screen.dart';

class HomeScreen extends StatefulWidget {
  final AppDatabase db;
  const HomeScreen({super.key, required this.db});
  @override State<HomeScreen> createState() => _HomeState();
}

class _HomeState extends State<HomeScreen> {
  int tab = 0;
  late Future<Map<String,dynamic>> child;
  String language = 'ar';
  String age = '6-7';

  @override
  void initState() {
    super.initState();
    child = widget.db.child();
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    language = await widget.db.setting('selected_language','ar');
    age = await widget.db.setting('selected_age','6-7');
    if (mounted) setState(() {});
  }

  Future<void> _selectLanguage(String value) async {
    await widget.db.setSetting('selected_language',value);
    if (mounted) setState(() => language = value);
  }

  @override
  Widget build(BuildContext context) {
    final pages = <Widget>[
      _dashboard(),
      LearnScreen(db: widget.db),
      GamesScreen(db: widget.db),
      StoriesScreen(db: widget.db, language: language, ageGroup: age),
      ParentScreen(db: widget.db),
    ];
    return Directionality(
      textDirection: TextDirection.rtl,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('لغتي', style: TextStyle(fontWeight: FontWeight.bold)),
          actions: [
            PopupMenuButton<String>(
              onSelected: _selectLanguage,
              itemBuilder: (_) => const [
                PopupMenuItem(value: 'ar', child: Text('الأكاديمية العربية')),
                PopupMenuItem(value: 'en', child: Text('الأكاديمية الإنجليزية')),
              ],
            ),
            IconButton(
              icon: const Icon(Icons.video_library_outlined),
              onPressed: () => Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => MediaScreen(db: widget.db)),
              ),
            ),
          ],
        ),
        body: pages[tab],
        bottomNavigationBar: NavigationBar(
          selectedIndex: tab,
          onDestinationSelected: (i) => setState(() => tab = i),
          destinations: const [
            NavigationDestination(icon: Icon(Icons.home_outlined), label: 'الرئيسية'),
            NavigationDestination(icon: Icon(Icons.school_outlined), label: 'التعلم'),
            NavigationDestination(icon: Icon(Icons.sports_esports_outlined), label: 'الألعاب'),
            NavigationDestination(icon: Icon(Icons.menu_book_outlined), label: 'القصص'),
            NavigationDestination(icon: Icon(Icons.family_restroom_outlined), label: 'ولي الأمر'),
          ],
        ),
      ),
    );
  }

  Widget _dashboard() => FutureBuilder<Map<String,dynamic>>(
    future: child,
    builder: (context, snapshot) {
      if (!snapshot.hasData) return const Center(child: CircularProgressIndicator());
      final name = snapshot.data!['name'].toString();
      return ListView(
        padding: const EdgeInsets.all(18),
        children: [
          Text(
            'مرحباً ' + name + ' 👋',
            style: Theme.of(context).textTheme.headlineMedium?.copyWith(fontWeight: FontWeight.bold),
          ),
          Text(language == 'ar' ? 'الأكاديمية العربية' : 'English Academy'),
          const SizedBox(height: 16),
          _card('🎯 خطة اليوم','درس + مفردات + لعبة + قصة + مراجعة',Icons.today,1),
          _card('🗺️ المنهج','13 مستوى × 6 مهارات × 5 فئات عمرية',Icons.map,1),
          _card('🎮 الألعاب','تدريب وتكرار ومراجعة',Icons.sports_esports,2),
          _card('📖 القصص','قصص متدرجة وأسئلة فهم',Icons.auto_stories,3),
          _card('🎬 الوسائط','صوت الجهاز ووسائط أصلية أو مرخّصة',Icons.video_library,0),
          const SizedBox(height: 8),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('الفئة العمرية', style: TextStyle(fontWeight: FontWeight.bold)),
                  Wrap(
                    spacing: 6,
                    children: ['4-5','6-7','8-10','11-13','14+'].map(
                      (x) => ChoiceChip(
                        label: Text(x),
                        selected: age == x,
                        onSelected: (selected) async {
                          if (!selected) return;
                          await widget.db.setSetting('selected_age',x);
                          if (mounted) setState(() => age = x);
                        },
                      ),
                    ).toList(),
                  ),
                ],
              ),
            ),
          ),
        ],
      );
    },
  );

  Widget _card(String title,String subtitle,IconData icon,int page) => Card(
    child: ListTile(
      leading: CircleAvatar(child: Icon(icon)),
      title: Text(title),
      subtitle: Text(subtitle),
      trailing: const Icon(Icons.chevron_left),
      onTap: () => setState(() => tab = page),
    ),
  );
}
