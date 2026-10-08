import 'package:flutter_test/flutter_test.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';
import 'package:lughati_mobile/main.dart';
import 'package:lughati_mobile/data/app_database.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  sqfliteFfiInit();
  databaseFactory = databaseFactoryFfi;

  testWidgets('واجهة لغتي تفتح', (tester) async {
    final db = await AppDatabase.open(path: inMemoryDatabasePath);
    await tester.pumpWidget(LughatiApp(db: db));
    await tester.pumpAndSettle(const Duration(seconds: 2));
    expect(find.text('لغتي'), findsOneWidget);
    expect(find.text('خطة اليوم'), findsOneWidget);
    expect(find.text('التعلم'), findsOneWidget);
  });
}
