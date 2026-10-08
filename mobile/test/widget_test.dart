import 'package:flutter_test/flutter_test.dart';
import 'package:lughati_mobile/main.dart';

void main() {
  testWidgets('واجهة لغتي تفتح', (tester) async {
    await tester.pumpWidget(const LughatiApp.preview());
    await tester.pump();
    expect(find.text('لغتي'), findsOneWidget);
    expect(find.text('خطة اليوم'), findsOneWidget);
  });
}
