import 'package:flutter/material.dart';
import '../data/app_database.dart';

class MoreScreen extends StatefulWidget {
  final AppDatabase db;
  final String language;
  final String ageGroup;
  const MoreScreen({super.key,required this.db,required this.language,required this.ageGroup});
  @override State<MoreScreen> createState()=>_MoreState();
}
class _MoreState extends State<MoreScreen>{
  final search=TextEditingController();
  String tab='dictionary';
  @override void dispose(){search.dispose();super.dispose();}
  @override Widget build(BuildContext context)=>ListView(padding:const EdgeInsets.all(16),children:[
    Text('⚙️ أدوات لغتي',style:Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight:FontWeight.bold)),
    const SizedBox(height:12),
    Wrap(spacing:8,runSpacing:8,children:[
      _chip('القاموس','dictionary'),_chip('التقييم','assessment'),_chip('الخطة','plan'),_chip('المستويات','levels'),_chip('الإنجازات','achievements'),_chip('الإعدادات','settings'),_chip('المساعد','assistant'),_chip('النطق','pronunciation'),
    ]),
    const SizedBox(height:14),_body(),
  ]);
  Widget _chip(String text,String value)=>ChoiceChip(label:Text(text),selected:tab==value,onSelected:(_){setState(()=>tab=value);});
  Widget _body(){
    switch(tab){
      case 'dictionary': return _dictionary();
      case 'assessment': return _assessment();
      case 'plan': return _plan();
      case 'levels': return _levels();
      case 'achievements': return _achievements();
      case 'settings': return _settings();
      case 'assistant': return _assistant();
      case 'pronunciation': return _pronunciation();
      default:return const SizedBox.shrink();
    }
  }
  Widget _dictionary()=>Column(crossAxisAlignment:CrossAxisAlignment.stretch,children:[
    TextField(controller:search,decoration:const InputDecoration(labelText:'ابحث عن كلمة',prefixIcon:Icon(Icons.search),border:OutlineInputBorder()),onChanged:(_){setState((){});}),
    const SizedBox(height:8),
    FutureBuilder<List<Map<String,dynamic>>>(future:widget.db.words(widget.language,query:search.text),builder:(c,s){
      if(!s.hasData)return const Center(child:CircularProgressIndicator());
      return Column(children:s.data!.map((w)=>Card(child:ListTile(title:Text(w['text'].toString(),style:const TextStyle(fontSize:20,fontWeight:FontWeight.bold)),subtitle:Text(w['meaning'].toString()+'\n'+w['example'].toString())))).toList());
    })
  ]);
  Widget _assessment()=>FutureBuilder<Map<String,dynamic>>(future:_stats(),builder:(c,s){
    if(!s.hasData)return const CircularProgressIndicator();final x=s.data!;
    return Card(child:Padding(padding:const EdgeInsets.all(16),child:Column(children:[
      const Text('تقييم المهارات',style:TextStyle(fontSize:20,fontWeight:FontWeight.bold)),
      _bar('الاستماع',x['listening']),_bar('التحدث',x['speaking']),_bar('القراءة',x['reading']),_bar('الكتابة',x['writing']),_bar('المفردات',x['vocabulary']),_bar('النحو',x['grammar']),
    ])));
  });
  Future<Map<String,dynamic>> _stats()async{
    final c=await widget.db.child();final id=c['id'] as int;final rows=await widget.db.attempts(id);final result=<String,double>{'listening':0,'speaking':0,'reading':0,'writing':0,'vocabulary':0,'grammar':0};final count=<String,int>{for(final k in result.keys)k:0};
    for(final r in rows){final k=r['kind'].toString();if(result.containsKey(k)){result[k]=(result[k]!+((r['score'] as num).toDouble()));count[k]=count[k]!+1;}}
    return {for(final k in result.keys)k:count[k]==0?0:(result[k]!/count[k]!).round()};
  }
  Widget _bar(String title,dynamic value)=>Padding(padding:const EdgeInsets.symmetric(vertical:5),child:Row(children:[SizedBox(width:70,child:Text(title)),Expanded(child:LinearProgressIndicator(value:((value as num).toDouble()/100).clamp(0,1))),const SizedBox(width:8),Text(value.toString()+'%')]));
  Widget _plan()=>FutureBuilder<Map<String,dynamic>>(future:widget.db.child(),builder:(c,s){
    if(!s.hasData)return const CircularProgressIndicator();
    final id=s.data!['id'] as int;
    return FutureBuilder<List<Map<String,dynamic>>>(future:widget.db.dailyTasks(id),builder:(c,t){
      if(!t.hasData)return const CircularProgressIndicator();
      return Column(children:t.data!.map((x)=>Card(child:CheckboxListTile(value:x['done']==1,title:Text(x['title'].toString()),subtitle:Text(x['minutes'].toString()+' دقيقة'),onChanged:(v)async{await widget.db.toggleTask(x['id'] as int,v==true?1:0);setState((){});}))).toList());
    });
  });
  Widget _levels()=>FutureBuilder<List<Map<String,dynamic>>>(future:widget.db.levelSummary(widget.language,widget.ageGroup),builder:(c,s){
    if(!s.hasData)return const CircularProgressIndicator();
    return Column(children:s.data!.map((x)=>Card(child:ListTile(leading:CircleAvatar(child:Text(x['level'].toString())),title:Text('المستوى '+x['level'].toString()),subtitle:Text(x['lessons'].toString()+' وحدات منهجية')))).toList());
  });
  Widget _achievements()=>FutureBuilder<Map<String,dynamic>>(future:_achievementData(),builder:(c,s){
    if(!s.hasData)return const CircularProgressIndicator();final list=s.data!['items'] as List<Map<String,dynamic>>;
    return Column(children:list.map((a)=>Card(child:ListTile(leading:Icon(a['earned']==1?Icons.emoji_events:Icons.lock),title:Text(a['title'].toString()),subtitle:Text(a['description'].toString())))).toList());
  });
  Future<Map<String,dynamic>> _achievementData()async{final c=await widget.db.child();return {'items':await widget.db.allAchievements(c['id'] as int)};}
  Widget _settings()=>const Card(child:Column(children:[
    ListTile(title:Text('العمل دون إنترنت'),subtitle:Text('الدروس والتقدم المحليان يعملان دون اتصال.')),
    ListTile(title:Text('الخصوصية'),subtitle:Text('بيانات التعلم محفوظة محلياً على الجهاز.')),
    ListTile(title:Text('المزامنة'),subtitle:Text('اختيارية عند توفر الإنترنت.')),
  ]));
  Widget _assistant()=>Card(child:Padding(padding:const EdgeInsets.all(16),child:Column(crossAxisAlignment:CrossAxisAlignment.stretch,children:[
    const Text('🤖 مساعد لغتي',style:TextStyle(fontSize:20,fontWeight:FontWeight.bold)),const SizedBox(height:8),
    const Text('مساعد تعليمي للسؤال والتوضيح والمراجعة.'),const SizedBox(height:10),
    Wrap(spacing:6,children:['اشرح الكلمة','أعطني مثالاً','اختبرني','راجع معي'].map((x)=>ActionChip(label:Text(x),onPressed:()=>ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('سنبدأ: '+x))))).toList()),
  ])));
  Widget _pronunciation()=>Card(child:Padding(padding:const EdgeInsets.all(16),child:Column(children:[
    const Text('🎙️ مختبر النطق',style:TextStyle(fontSize:20,fontWeight:FontWeight.bold)),const SizedBox(height:8),
    Text(widget.language=='ar'?'قل: كتاب، مدرسة، شمس':'Say: book, school, sun'),const SizedBox(height:12),
    const Text('التحليل الصوتي الفونيمي الحقيقي يحتاج نموذج نطق مخصصاً؛ بقية المنهج يعمل دون اتصال.'),
  ])));
}
