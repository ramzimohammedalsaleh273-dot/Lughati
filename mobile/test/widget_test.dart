import 'package:flutter_test/flutter_test.dart';import 'package:lughati_mobile/main.dart';import 'package:lughati_mobile/data/app_database.dart';
void main(){testWidgets('واجهة لغتي تفتح',(tester)async{final db=await AppDatabase.open();await tester.pumpWidget(LughatiApp(db:db));await tester.pumpAndSettle();expect(find.text('لغتي'),findsOneWidget);expect(find.text('خطة اليوم'),findsOneWidget);});}
