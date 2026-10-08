import 'package:flutter/material.dart';
import 'data/app_database.dart';
import 'screens/home_screen.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final db = await AppDatabase.open();
  runApp(LughatiApp(db: db));
}

class LughatiApp extends StatelessWidget {
  final AppDatabase? db;
  final bool preview;
  const LughatiApp({super.key, required this.db}) : preview = false;
  const LughatiApp.preview({super.key}) : db = null, preview = true;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner:false,
      title:'لغتي',
      theme:ThemeData(useMaterial3:true,colorSchemeSeed:const Color(0xFF6750A4)),
      home: preview
          ? const Directionality(textDirection:TextDirection.rtl,child:Scaffold(
              appBar:AppBar(title:Text('لغتي')),
              body:Center(child:Text('خطة اليوم',style:TextStyle(fontSize:24,fontWeight:FontWeight.bold))),
            ))
          : Directionality(textDirection:TextDirection.rtl,child:HomeScreen(db:db!)),
    );
  }
}
