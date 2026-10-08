import 'package:flutter/material.dart';
import '../data/app_database.dart';
import 'learn_screen.dart';
import 'games_screen.dart';
import 'stories_screen.dart';
import 'parent_screen.dart';
import 'media_screen.dart';

class HomeScreen extends StatefulWidget{final AppDatabase db;const HomeScreen({super.key,required this.db});@override State<HomeScreen> createState()=>_HomeState();}
class _HomeState extends State<HomeScreen>{
 int tab=0;late Future<Map<String,dynamic>> child;
 @override void initState(){super.initState();child=widget.db.child();}
 @override Widget build(BuildContext context){
  final pages=[dashboard(),LearnScreen(db:widget.db),GamesScreen(db:widget.db),StoriesScreen(db:widget.db),ParentScreen(db:widget.db)];
  return Directionality(textDirection:TextDirection.rtl,child:Scaffold(
   appBar:AppBar(title:const Text('لغتي'),actions:[IconButton(icon:const Icon(Icons.video_library_outlined),onPressed:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>MediaScreen(db:widget.db))))]),
   body:pages[tab],
   bottomNavigationBar:NavigationBar(selectedIndex:tab,onDestinationSelected:(i)=>setState(()=>tab=i),destinations:const[
    NavigationDestination(icon:Icon(Icons.home_outlined),label:'الرئيسية'),NavigationDestination(icon:Icon(Icons.school_outlined),label:'التعلم'),NavigationDestination(icon:Icon(Icons.sports_esports_outlined),label:'الألعاب'),NavigationDestination(icon:Icon(Icons.menu_book_outlined),label:'القصص'),NavigationDestination(icon:Icon(Icons.family_restroom_outlined),label:'ولي الأمر')]))
  );}
 Widget dashboard()=>FutureBuilder<Map<String,dynamic>>(future:child,builder:(c,s){
  if(!s.hasData)return const Center(child:CircularProgressIndicator());
  final name=s.data!['name'].toString();
  return ListView(padding:const EdgeInsets.all(20),children:[
   Text('مرحباً '+name+' 👋',style:Theme.of(context).textTheme.headlineMedium?.copyWith(fontWeight:FontWeight.bold)),
   const SizedBox(height:8),const Text('مدرسة اللغات العربية والإنجليزية — تعمل دون اتصال.'),
   const SizedBox(height:20),card('🎯 خطة اليوم','درس + كلمات + لعبة + مراجعة',Icons.today,1),
   card('🗺️ خريطة التعلم','13 مستوى × 6 مهارات',Icons.map,1),
   card('🎬 ليان وسامي','الدروس المرئية التفاعلية',Icons.ondemand_video,1),
   card('🏆 الإنجازات','تعلم، راجع، وأتقن',Icons.emoji_events,1)]);
 });
 Widget card(String title,String sub,IconData icon,int page)=>Card(child:ListTile(leading:CircleAvatar(child:Icon(icon)),title:Text(title),subtitle:Text(sub),trailing:TextButton(onPressed:()=>setState(()=>tab=page),child:const Text('ابدأ'))));
}
