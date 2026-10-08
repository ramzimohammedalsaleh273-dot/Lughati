import 'package:path/path.dart' as p;
import 'package:sqflite/sqflite.dart';

class AppDatabase {
  final Database db;
  AppDatabase._(this.db);
  static Future<AppDatabase> open() async {
    final path=p.join(await getDatabasesPath(),'lughati.db');
    final db=await openDatabase(path,version:1,onCreate:(db,v) async {
      await db.execute('CREATE TABLE children(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,age INTEGER NOT NULL)');
      await db.execute('CREATE TABLE lessons(id INTEGER PRIMARY KEY AUTOINCREMENT,language TEXT,level INTEGER,title TEXT,skill TEXT,body TEXT)');
      await db.execute('CREATE TABLE progress(id INTEGER PRIMARY KEY AUTOINCREMENT,child_id INTEGER,lesson_id INTEGER,score REAL,mastered INTEGER,updated_at TEXT)');
      await db.execute('CREATE TABLE words(id INTEGER PRIMARY KEY AUTOINCREMENT,language TEXT,text TEXT,meaning TEXT,example TEXT,level INTEGER)');
      await db.execute('CREATE TABLE settings(key TEXT PRIMARY KEY,value TEXT)');
      await db.insert('children',{'name':'الطفل','age':6});
      const ar=['الحروف والأصوات','الكلمات الأولى','القراءة','الكتابة','الجمل','الفهم','المحادثة','المفردات','النحو','القصص','الإملاء','التعبير','المراجعة'];
      const en=['Alphabet & Phonics','First Words','Reading','Writing','Sentences','Comprehension','Conversation','Vocabulary','Grammar','Stories','Spelling','Expression','Review'];
      const skills=['listening','speaking','reading','writing','vocabulary','grammar'];
      for(var level=0;level<13;level++){for(final lang in ['ar','en']){final title=lang=='ar'?ar[level]:en[level];for(final skill in skills){await db.insert('lessons',{'language':lang,'level':level,'title':title,'skill':skill,'body':lang=='ar'?'درس المستوى '+level.toString()+' — '+title+'. استمع، شاهد النموذج، تدرب، ثم أثبت الإتقان.':'Level '+level.toString()+' — '+title+'. Listen, study the model, practise, then demonstrate mastery.'});}}}
      const arWords=['كتاب','قلم','مدرسة','بيت','أسرة','طعام','ماء','شمس','قمر','حيوان','مدينة','وقت','صديق'];
      const enWords=['book','pen','school','home','family','food','water','sun','moon','animal','city','time','friend'];
      for(final w in arWords){await db.insert('words',{'language':'ar','text':w,'meaning':w,'example':'كلمة: '+w,'level':0});}
      for(final w in enWords){await db.insert('words',{'language':'en','text':w,'meaning':w,'example':'Word: '+w,'level':0});}
    });
    return AppDatabase._(db);
  }
  Future<Map<String,dynamic>> child() async=>(await db.query('children',limit:1)).first;
  Future<List<Map<String,dynamic>>> lessons(String lang)=>db.query('lessons',where:'language=?',whereArgs:[lang],orderBy:'level,id');
  Future<List<Map<String,dynamic>>> words(String lang)=>db.query('words',where:'language=?',whereArgs:[lang],orderBy:'level,id');
  Future<int> completeLesson(int childId,int lessonId,double score)=>db.insert('progress',{'child_id':childId,'lesson_id':lessonId,'score':score,'mastered':score>=80?1:0,'updated_at':DateTime.now().toIso8601String()});
  Future<int> completedCount(int childId) async {final r=await db.rawQuery('SELECT COUNT(DISTINCT lesson_id) c FROM progress WHERE child_id=?',[childId]);return (r.first['c'] as int?)??0;}
}
