# iPhone 17 / iPad 10 Auto Clicker

iPhone 17 및 iPad 10세대를 대상으로 하는 간단한 iOS 자동 터치 GUI 앱입니다.

## 중요한 현실 체크
이 프로젝트는 **Android ADB처럼 바로 되는 구조가 아닙니다.**  
iPhone/iPad 자동 제어는 Apple 보안 구조상 더 까다롭습니다.

즉, 이 프로젝트는 **Windows 단독보다는 macOS 환경에서 더 안정적**입니다.

---

## 지원 개념
- 연결된 iPhone/iPad 감지
- 특정 좌표 1회 터치
- 반복 자동 터치
- 스와이프 테스트
- Bundle ID로 앱 실행
- iPhone 17 / iPad 10 프리셋 저장

---

## 권장 환경
- **macOS**
- Python 3.10+
- Xcode 또는 iOS 개발 도구 일부 설치 권장
- USB 연결된 iPhone / iPad
- 기기 신뢰 허용

---

## 설치
```bash
pip install -r requirements.txt
```

## 의존 도구
이 프로젝트는 기본적으로 `tidevice` 기반입니다.

연결 확인:
```bash
tidevice list
```

기기가 보이면 연결은 된 것입니다.

---

## 실행
```bash
python main.py
```

---

## 좌표 개념
Android처럼 ADB tap이 아니라, iOS 자동화 도구를 통해 화면 좌표를 터치하는 구조입니다.

즉:
- iPhone 17용 프리셋
- iPad 10세대용 프리셋

을 나눠서 저장해두고 쓸 수 있습니다.

---

## 기본 프리셋
### iPhone 17
- X = 200
- Y = 600

### iPad 10
- X = 300
- Y = 800

이 값은 **샘플값**입니다.  
실제 앱 자동화용 좌표는 직접 맞춰야 합니다.

---

## 앱 실행 예시
설정 앱 실행:
```text
com.apple.Preferences
```

---

## 한계
Apple 쪽은 Android보다 자동화가 훨씬 까다롭습니다.

특히:
- 앱별 접근 제한
- 좌표 불일치
- iOS 버전별 차이
- 개발자 도구/서명 이슈

가 있을 수 있습니다.

즉, 이 저장소는 **토대용 프로젝트**로 보는 게 맞습니다.

---

## 다음에 붙이기 좋은 기능
- 여러 좌표 순차 클릭
- 루프 시퀀스 저장
- 랜덤 간격
- 기기별 해상도 프로필
- EXE / 앱 패키징
- 더 안정적인 iOS 제어 레이어
