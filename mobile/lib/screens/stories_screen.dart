import 'package:flutter/material.dart';
import '../data/app_database.dart';

class StoriesScreen extends StatefulWidget {
  final AppDatabase db;
  final String language;
  final String ageGroup;
  const StoriesScreen({super.key, required this.db, required this.language, required this.ageGroup});
  @override State<StoriesScreen> createState()=>_StoriesState();
}

class _StoriesState extends State<StoriesScreen>{
  late Future<List<Map<String,dynamic>>> data;
  int level=0;
  @override void initState(){super.initState();data=widget.db.stories(widget.language,age:widget.ageGroup,level:level);}
  void _load(){setState(()=>data=widget.db.stories(widget.language,age:widget.ageGroup,level:level));}
  @override Widget build(BuildContext context)=>ListView(padding:const EdgeInsets.all(16),children:[
    Text('📖 مكتبة القصص',style:Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight:FontWeight.bold)),
    const SizedBox(height:8),
    const Text('استمع، اقرأ، أجب عن أسئلة الفهم، ثم سجّل إتمام القصة.'),
    const SizedBox(height:10),
    SizedBox(height:52,child:ListView.separated(scrollDirection:Axis.horizontal,itemCount:13,separatorBuilder:(_,__)=>const SizedBox(width:6),itemBuilder:(c,i)=>ChoiceChip(label:Text(i.toString()),selected:level==i,onSelected:(_){level=i;_load();}))),
    const SizedBox(height:8),
    FutureBuilder<List<Map<String,dynamic>>>(future:data,builder:(c,s){
      if(s.hasError)return Text('تعذر تحميل القصص: '+s.error.toString());
      if(!s.hasData)return const Center(child:CircularProgressIndicator());
      return Column(children:s.data!.map((story)=>Card(child:ListTile(
        leading:CircleAvatar(child:Text(story['level'].toString())),
        title:Text(story['title'].toString()),
        subtitle:Text(story['moral'].toString()),
        trailing:const Icon(Icons.auto_stories),
        onTap:()=>_open(story),
      ))).toList());
    }),
  ]);
  Future<void> _open(Map<String,dynamic> story)async{
    final qs=await widget.db.storyQuestions(story['id'] as int);
    if(!mounted)return;
    await showDialog(context:context,builder:(ctx)=>AlertDialog(
      title:Text(story['title'].toString()),
      content:SizedBox(width:420,child:ListView(shrinkWrap:true,children:[
        Text(story['body'].toString()),
        const SizedBox(height:12),
        ...qs.map((q)=>Card(child:Padding(padding:const EdgeInsets.all(10),child:Text(q['prompt'].toString()+'\n'+q['options'].toString().replaceAll('|',' • ')))))
      ])),
      actions:[TextButton(onPressed:()async{
        final ch=await widget.db.child();
        await widget.db.recordAttempt(ch['id'] as int,story['id'] as int,'story',100,'completed');
        if(ctx.mounted)Navigator.pop(ctx);
      },child:const Text('تمت القصة'))],
    ));
  }
}
