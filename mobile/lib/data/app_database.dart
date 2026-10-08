import 'package:path/path.dart' as p;
import 'package:sqflite/sqflite.dart';

class AppDatabase {
  final Database db;
  AppDatabase._(this.db);

  static Future<AppDatabase> open({String? path}) async {
    final dbPath = path ?? p.join(await getDatabasesPath(), 'lughati.db');
    final database = await openDatabase(
      dbPath,
      version: 2,
      onCreate: _create,
      onUpgrade: _upgrade,
    );
    return AppDatabase._(database);
  }

  static Future<void> _create(Database db, int version) async {
    await db.execute('CREATE TABLE children(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,age INTEGER NOT NULL,language TEXT NOT NULL DEFAULT "ar")');
    await db.execute('CREATE TABLE lessons(id INTEGER PRIMARY KEY AUTOINCREMENT,language TEXT NOT NULL,age_group TEXT NOT NULL,level INTEGER NOT NULL,title TEXT NOT NULL,skill TEXT NOT NULL,objective TEXT NOT NULL,body TEXT NOT NULL)');
    await db.execute('CREATE TABLE lesson_steps(id INTEGER PRIMARY KEY AUTOINCREMENT,lesson_id INTEGER NOT NULL,step_no INTEGER NOT NULL,kind TEXT NOT NULL,prompt TEXT NOT NULL,answer TEXT,options TEXT)');
    await db.execute('CREATE TABLE progress(id INTEGER PRIMARY KEY AUTOINCREMENT,child_id INTEGER NOT NULL,lesson_id INTEGER NOT NULL,score REAL NOT NULL,mastered INTEGER NOT NULL DEFAULT 0,attempts INTEGER NOT NULL DEFAULT 1,updated_at TEXT NOT NULL,UNIQUE(child_id,lesson_id))');
    await db.execute('CREATE TABLE words(id INTEGER PRIMARY KEY AUTOINCREMENT,language TEXT NOT NULL,text TEXT NOT NULL,meaning TEXT NOT NULL,example TEXT NOT NULL,level INTEGER NOT NULL,topic TEXT NOT NULL)');
    await db.execute('CREATE TABLE stories(id INTEGER PRIMARY KEY AUTOINCREMENT,language TEXT NOT NULL,age_group TEXT NOT NULL,level INTEGER NOT NULL,title TEXT NOT NULL,body TEXT NOT NULL,moral TEXT NOT NULL)');
    await db.execute('CREATE TABLE story_questions(id INTEGER PRIMARY KEY AUTOINCREMENT,story_id INTEGER NOT NULL,prompt TEXT NOT NULL,answer TEXT NOT NULL,options TEXT NOT NULL)');
    await db.execute('CREATE TABLE attempts(id INTEGER PRIMARY KEY AUTOINCREMENT,child_id INTEGER NOT NULL,lesson_id INTEGER,kind TEXT NOT NULL,score REAL NOT NULL,details TEXT NOT NULL,created_at TEXT NOT NULL)');
    await db.execute('CREATE TABLE achievements(id INTEGER PRIMARY KEY AUTOINCREMENT,code TEXT UNIQUE NOT NULL,title TEXT NOT NULL,description TEXT NOT NULL)');
    await db.execute('CREATE TABLE child_achievements(child_id INTEGER NOT NULL,achievement_id INTEGER NOT NULL,earned_at TEXT NOT NULL,PRIMARY KEY(child_id,achievement_id))');
    await db.execute('CREATE TABLE daily_tasks(id INTEGER PRIMARY KEY AUTOINCREMENT,child_id INTEGER NOT NULL,title TEXT NOT NULL,kind TEXT NOT NULL,done INTEGER NOT NULL DEFAULT 0,minutes INTEGER NOT NULL,day TEXT NOT NULL)');
    await db.execute('CREATE TABLE media(id INTEGER PRIMARY KEY AUTOINCREMENT,language TEXT NOT NULL,type TEXT NOT NULL,title TEXT NOT NULL,path TEXT,source TEXT,offline INTEGER NOT NULL DEFAULT 0)');
    await db.execute('CREATE TABLE settings(key TEXT PRIMARY KEY,value TEXT NOT NULL)');
    await _seed(db);
  }

  static Future<void> _upgrade(Database db, int oldVersion, int newVersion) async {
    if (oldVersion < 2) {
      final info = await db.rawQuery('PRAGMA table_info(lessons)');
      final hasAge = info.any((r) => r['name'] == 'age_group');
      if (!hasAge) {
        await db.execute('ALTER TABLE lessons ADD COLUMN age_group TEXT NOT NULL DEFAULT "6-7"');
      }
      await db.execute('CREATE TABLE IF NOT EXISTS lesson_steps(id INTEGER PRIMARY KEY AUTOINCREMENT,lesson_id INTEGER NOT NULL,step_no INTEGER NOT NULL,kind TEXT NOT NULL,prompt TEXT NOT NULL,answer TEXT,options TEXT)');
      await db.execute('CREATE TABLE IF NOT EXISTS stories(id INTEGER PRIMARY KEY AUTOINCREMENT,language TEXT NOT NULL,age_group TEXT NOT NULL,level INTEGER NOT NULL,title TEXT NOT NULL,body TEXT NOT NULL,moral TEXT NOT NULL)');
      await db.execute('CREATE TABLE IF NOT EXISTS story_questions(id INTEGER PRIMARY KEY AUTOINCREMENT,story_id INTEGER NOT NULL,prompt TEXT NOT NULL,answer TEXT NOT NULL,options TEXT NOT NULL)');
      await db.execute('CREATE TABLE IF NOT EXISTS attempts(id INTEGER PRIMARY KEY AUTOINCREMENT,child_id INTEGER NOT NULL,lesson_id INTEGER,kind TEXT NOT NULL,score REAL NOT NULL,details TEXT NOT NULL,created_at TEXT NOT NULL)');
      await db.execute('CREATE TABLE IF NOT EXISTS achievements(id INTEGER PRIMARY KEY AUTOINCREMENT,code TEXT UNIQUE NOT NULL,title TEXT NOT NULL,description TEXT NOT NULL)');
      await db.execute('CREATE TABLE IF NOT EXISTS child_achievements(child_id INTEGER NOT NULL,achievement_id INTEGER NOT NULL,earned_at TEXT NOT NULL,PRIMARY KEY(child_id,achievement_id))');
      await db.execute('CREATE TABLE IF NOT EXISTS daily_tasks(id INTEGER PRIMARY KEY AUTOINCREMENT,child_id INTEGER NOT NULL,title TEXT NOT NULL,kind TEXT NOT NULL,done INTEGER NOT NULL DEFAULT 0,minutes INTEGER NOT NULL,day TEXT NOT NULL)');
      await db.execute('CREATE TABLE IF NOT EXISTS media(id INTEGER PRIMARY KEY AUTOINCREMENT,language TEXT NOT NULL,type TEXT NOT NULL,title TEXT NOT NULL,path TEXT,source TEXT,offline INTEGER NOT NULL DEFAULT 0)');
      await db.execute('CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value TEXT NOT NULL)');
      await _seedExtra(db);
    }
  }

  static Future<void> _seed(Database db) async {
    await db.insert('children', {'name':'الطفل','age':6,'language':'ar'});
    const arTitles=['الحروف والأصوات','الكلمات الأولى','القراءة','الكتابة','الجمل','الفهم','المحادثة','المفردات','النحو','القصص','الإملاء','التعبير','المراجعة'];
    const enTitles=['Alphabet & Phonics','First Words','Reading','Writing','Sentences','Comprehension','Conversation','Vocabulary','Grammar','Stories','Spelling','Expression','Review'];
    const skills=['listening','speaking','reading','writing','vocabulary','grammar'];
    const ages=['4-5','6-7','8-10','11-13','14+'];
    for (var level=0; level<13; level++) {
      for (final lang in ['ar','en']) {
        for (final age in ages) {
          for (final skill in skills) {
            final title = lang == 'ar' ? arTitles[level] : enTitles[level];
            final objective = lang == 'ar'
                ? 'إتقان مهارة ' + skill + ' في موضوع ' + title
                : 'Build ' + skill + ' skill through ' + title;
            final lessonId = await db.insert('lessons', {
              'language':lang,'age_group':age,'level':level,'title':title,'skill':skill,
              'objective':objective,
              'body':lang == 'ar'
                  ? 'درس متدرج للفئة ' + age + ' في المستوى ' + level.toString() + '. تعلّم، تدرب، طبّق، ثم أثبت الإتقان.'
                  : 'A guided lesson for age ' + age + ' at level ' + level.toString() + '. Learn, practise, apply, then demonstrate mastery.'
            });
            for (var step=1; step<=4; step++) {
              await db.insert('lesson_steps',{
                'lesson_id':lessonId,'step_no':step,
                'kind':step==4?'assessment':'practice',
                'prompt':lang == 'ar'
                    ? 'نشاط ' + step.toString() + ': استمع ثم طبّق المهارة.'
                    : 'Activity ' + step.toString() + ': listen and apply the skill.',
                'answer':null,'options':null
              });
            }
          }
        }
      }
    }
    await _seedWords(db);
    await _seedStories(db);
    await _seedAchievements(db);
    await _seedTasks(db,1);
    await _seedMedia(db);
    await db.insert('settings',{'key':'selected_age','value':'6-7'});
    await db.insert('settings',{'key':'selected_language','value':'ar'});
    await db.insert('settings',{'key':'offline_first','value':'true'});
  }

  static Future<void> _seedExtra(Database db) async {
    final lessonCount = ((await db.rawQuery('SELECT COUNT(*) c FROM lessons')).first['c'] as int?) ?? 0;
    if (lessonCount < 780) {
      const arTitles=['الحروف والأصوات','الكلمات الأولى','القراءة','الكتابة','الجمل','الفهم','المحادثة','المفردات','النحو','القصص','الإملاء','التعبير','المراجعة'];
      const enTitles=['Alphabet & Phonics','First Words','Reading','Writing','Sentences','Comprehension','Conversation','Vocabulary','Grammar','Stories','Spelling','Expression','Review'];
      const skills=['listening','speaking','reading','writing','vocabulary','grammar'];
      const ages=['4-5','6-7','8-10','11-13','14+'];
      for (var level=0; level<13; level++) {
        for (final lang in ['ar','en']) {
          for (final age in ages) {
            for (final skill in skills) {
              final exists=await db.query('lessons',where:'language=? AND age_group=? AND level=? AND skill=?',whereArgs:[lang,age,level,skill],limit:1);
              if(exists.isNotEmpty) continue;
              final title=lang=='ar'?arTitles[level]:enTitles[level];
              final id=await db.insert('lessons',{'language':lang,'age_group':age,'level':level,'title':title,'skill':skill,'objective':title,'body':title});
              for(var step=1;step<=4;step++){await db.insert('lesson_steps',{'lesson_id':id,'step_no':step,'kind':step==4?'assessment':'practice','prompt':title,'answer':null,'options':null});}
            }
          }
        }
      }
    }
    if (((await db.rawQuery('SELECT COUNT(*) c FROM stories')).first['c'] as int?) == 0) await _seedStories(db);
    if (((await db.rawQuery('SELECT COUNT(*) c FROM achievements')).first['c'] as int?) == 0) await _seedAchievements(db);
    final childRows=await db.query('children',limit:1);
    if(childRows.isNotEmpty) await _seedTasks(db,childRows.first['id'] as int);
    await _seedMedia(db);
  }

  static Future<void> _seedWords(Database db) async {
    const ar=['كتاب','قلم','مدرسة','بيت','أسرة','طعام','ماء','شمس','قمر','صديق','معلم','طفل','باب','كرسي','طاولة','سيارة','طريق','مدينة','حديقة','شجرة','زهرة','تفاحة','موز','حليب','خبز','بحر','جبل','سماء','نجمة','صباح','مساء','اليوم','غداً','سعيد','كبير','صغير','سريع','بطيء','جميل'];
    const en=['book','pen','school','home','family','food','water','sun','moon','friend','teacher','child','door','chair','table','car','road','city','garden','tree','flower','apple','banana','milk','bread','sea','mountain','sky','star','morning','evening','today','tomorrow','happy','big','small','fast','slow','beautiful'];
    for(final lang in ['ar','en']){
      final list=lang=='ar'?ar:en;
      for(var level=0;level<13;level++){
        for(var i=0;i<list.length;i++){
          final w=list[(i+level)%list.length];
          await db.insert('words',{'language':lang,'text':w,'meaning':lang=='ar'?'معنى '+w:'meaning of '+w,'example':lang=='ar'?'هذه جملة عن '+w:'This is a sentence about '+w,'level':level,'topic':level%2==0?'daily':'learning'});
        }
      }
    }
  }

  static Future<void> _seedStories(Database db) async {
    const ages=['4-5','6-7','8-10','11-13','14+'];
    for(final lang in ['ar','en']){
      for(final age in ages){
        for(var level=0;level<13;level++){
          final title=lang=='ar'?'مغامرة ليان وسامي — المستوى '+level.toString():'Lian and Sami Adventure — Level '+level.toString();
          final id=await db.insert('stories',{'language':lang,'age_group':age,'level':level,'title':title,'body':lang=='ar'?'ذهبت ليان وسامي إلى مكان جديد، لاحظا شيئاً مهماً، تعلما كلمة جديدة، ثم تحدثا عنها.':'Lian and Sami visited a new place, noticed something important, learned a new word, and talked about it.','moral':lang=='ar'?'التعلم بالملاحظة والتحدث والمراجعة.':'Learning grows through noticing, speaking, and reviewing.'});
          await db.insert('story_questions',{'story_id':id,'prompt':lang=='ar'?'من ذهب في الرحلة؟':'Who went on the trip?','answer':lang=='ar'?'ليان وسامي':'Lian and Sami','options':lang=='ar'?'ليان وسامي|شخص آخر|لا أحد':'Lian and Sami|Someone else|Nobody'});
          await db.insert('story_questions',{'story_id':id,'prompt':lang=='ar'?'ماذا تعلما؟':'What did they learn?','answer':lang=='ar'?'كلمة جديدة':'A new word','options':lang=='ar'?'كلمة جديدة|أغنية|لعبة':'A new word|A song|A game'});
        }
      }
    }
  }

  static Future<void> _seedAchievements(Database db) async {
    const a=[['first','أول درس','أكمل أول درس'],['five','خمسة دروس','أكمل خمسة دروس'],['perfect','إتقان','احصل على 100%'],['story','قارئ القصص','أكمل قصة'],['bilingual','ثنائي اللغة','تعلّم في اللغتين']];
    for(final x in a){await db.insert('achievements',{'code':x[0],'title':x[1],'description':x[2]},conflictAlgorithm:ConflictAlgorithm.ignore);}
  }

  static Future<void> _seedTasks(Database db,int childId) async {
    final day=DateTime.now().toIso8601String().substring(0,10);
    final exists=await db.query('daily_tasks',where:'child_id=? AND day=?',whereArgs:[childId,day],limit:1);
    if(exists.isNotEmpty)return;
    const t=[['درس جديد','lesson',15],['مفردات','vocabulary',10],['لعبة','game',10],['قصة','story',10],['مراجعة','review',10]];
    for(final x in t){await db.insert('daily_tasks',{'child_id':childId,'title':x[0],'kind':x[1],'minutes':x[2],'done':0,'day':day});}
  }

  static Future<void> _seedMedia(Database db) async {
    final count=((await db.rawQuery('SELECT COUNT(*) c FROM media')).first['c'] as int?)??0;
    if(count>0)return;
    await db.insert('media',{'language':'ar','type':'audio','title':'النطق العربي','source':'device_tts','offline':1});
    await db.insert('media',{'language':'en','type':'audio','title':'English pronunciation','source':'device_tts','offline':1});
    await db.insert('media',{'language':'ar','type':'video','title':'درس الحروف العربية المرخّص','source':'licensed_media','offline':0});
    await db.insert('media',{'language':'en','type':'video','title':'English learning video','source':'licensed_media','offline':0});
  }

  Future<Map<String,dynamic>> child() async => (await db.query('children',limit:1)).first;
  Future<List<Map<String,dynamic>>> lessons(String lang,{String? age,int? level,String? skill}) async {
    final w=['language=?']; final a=<Object?>[lang];
    if(age!=null){w.add('age_group=?');a.add(age);}
    if(level!=null){w.add('level=?');a.add(level);}
    if(skill!=null){w.add('skill=?');a.add(skill);}
    return db.query('lessons',where:w.join(' AND '),whereArgs:a,orderBy:'level,id');
  }
  Future<List<Map<String,dynamic>>> lessonSteps(int id)=>db.query('lesson_steps',where:'lesson_id=?',whereArgs:[id],orderBy:'step_no');
  Future<List<Map<String,dynamic>>> words(String lang,{int? level,String? query}) async {
    final w=['language=?']; final a=<Object?>[lang];
    if(level!=null){w.add('level=?');a.add(level);}
    if(query!=null&&query.trim().isNotEmpty){w.add('text LIKE ?');a.add('%'+query.trim()+'%');}
    return db.query('words',where:w.join(' AND '),whereArgs:a,orderBy:'level,text',limit:200);
  }
  Future<List<Map<String,dynamic>>> stories(String lang,{String? age,int? level}) async {
    final w=['language=?']; final a=<Object?>[lang];
    if(age!=null){w.add('age_group=?');a.add(age);}
    if(level!=null){w.add('level=?');a.add(level);}
    return db.query('stories',where:w.join(' AND '),whereArgs:a,orderBy:'level');
  }
  Future<List<Map<String,dynamic>>> storyQuestions(int id)=>db.query('story_questions',where:'story_id=?',whereArgs:[id]);
  Future<int> completeLesson(int childId,int lessonId,double score) async {
    final old=await db.query('progress',where:'child_id=? AND lesson_id=?',whereArgs:[childId,lessonId],limit:1);
    final data={'score':score,'mastered':score>=80?1:0,'updated_at':DateTime.now().toIso8601String()};
    if(old.isEmpty){data['child_id']=childId;data['lesson_id']=lessonId;data['attempts']=1;return db.insert('progress',data);}
    data['attempts']=(old.first['attempts'] as int)+1;
    return db.update('progress',data,where:'id=?',whereArgs:[old.first['id']]);
  }
  Future<void> recordAttempt(int childId,int? lessonId,String kind,double score,String details)=>db.insert('attempts',{'child_id':childId,'lesson_id':lessonId,'kind':kind,'score':score,'details':details,'created_at':DateTime.now().toIso8601String()});
  Future<int> completedCount(int childId) async=>((await db.rawQuery('SELECT COUNT(*) c FROM progress WHERE child_id=?',[childId])).first['c'] as int?)??0;
  Future<int> masteredCount(int childId) async=>((await db.rawQuery('SELECT COUNT(*) c FROM progress WHERE child_id=? AND mastered=1',[childId])).first['c'] as int?)??0;
  Future<double> averageScore(int childId) async=>(((await db.rawQuery('SELECT AVG(score) a FROM progress WHERE child_id=?',[childId])).first['a'] as num?)??0).toDouble();
  Future<List<Map<String,dynamic>>> dailyTasks(int childId) async{await _seedTasks(childId);final day=DateTime.now().toIso8601String().substring(0,10);return db.query('daily_tasks',where:'child_id=? AND day=?',whereArgs:[childId,day],orderBy:'id');}
  Future<void> toggleTask(int id,int done)=>db.update('daily_tasks',{'done':done},where:'id=?',whereArgs:[id]);
  Future<List<Map<String,dynamic>>> achievements(int childId)=>db.rawQuery('SELECT a.*,CASE WHEN ca.child_id IS NULL THEN 0 ELSE 1 END earned FROM achievements a LEFT JOIN child_achievements ca ON a.id=ca.achievement_id AND ca.child_id=? ORDER BY earned DESC,a.id',[childId]);
  Future<List<Map<String,dynamic>>> media(String lang)=>db.query('media',where:'language=?',whereArgs:[lang],orderBy:'type,id');
  Future<String> setting(String key,String fallback) async{final r=await db.query('settings',where:'key=?',whereArgs:[key],limit:1);return r.isEmpty?fallback:r.first['value'].toString();}
  Future<void> setSetting(String key,String value)=>db.insert('settings',{'key':key,'value':value},conflictAlgorithm:ConflictAlgorithm.replace);
}
