import 'package:flutter/material.dart';
import 'data/app_database.dart';
import 'screens/home_screen.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final db = await AppDatabase.open();
  runApp(LughatiApp(db: db));
}
class LughatiApp extends StatelessWidget {
  final AppDatabase db;
  const LughatiApp({super.key, required this.db});
  @override Widget build(BuildContext context) => MaterialApp(
    debugShowCheckedModeBanner:false, title:'لغتي',
    theme:ThemeData(useMaterial3:true, colorSchemeSeed:const Color(0xFF6750A4)),
    home:HomeScreen(db:db));
}
