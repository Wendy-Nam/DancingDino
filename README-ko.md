[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/) [![License: CC0-1.0](https://licensebuttons.net/l/zero/1.0/80x15.png)](http://creativecommons.org/publicdomain/zero/1.0/)
> KAU 2023 'Embedded Software 입문' 기말 프로젝트. `RaspberryPi4`와 `Adafruit 1.3" Color TFT Bonnet`을 사용한 리듬 게임

# Dancing Dino

⬇️ 썸네일을 클릭하여 비디오 시청

[![DancingDino](https://github.com/Wendy-Nam/DancingDino/blob/main/img/opening/14.png)](https://www.youtube.com/watch?v=G-tjcUxmIwA "댄싱다이노")

## 개요

"Dancing Dino"는 일종의 리듬 게임으로, 멋진 댄서가 되고 싶은 아기 공룡이 꿈을 이루는 스토리를 담고 있음

게임은 총 3개의 스테이지로 진행되며, 각 스테이지 별로 난이도(화살표의 속도)가 증가함

## 클래스와 기능
- `JoystickController`: 조이스틱 입력, 디스플레이 초기화 및 버튼 상태 업데이트 관리.
- `Player`: 플레이어의 스프라이트 이미지 관리, 포즈 업데이트 및 애니메이션 렌더링.
- `Arrow`: 화살표의 이동 및 렌더링 처리, 속도 및 방향 포함.
- `Stage`: 게임 단계 관리, 배경 렌더링, 점수 지역, 화살표 생성 및 단계 전환 포함.
- `Game`: 메인 게임 루프와 상태 컨트롤, 시작 화면, 업데이트 및 렌더링 포함.

## 게임 메커니즘
- 플레이어는 화면 상단에서 내려오는 화살표의 방향에 맞게 joystick을 조종.
- 정확한 타이밍&구간에서 화살표 방향을 맞추면 점수를 얻고, 그렇지 않으면 점수가 깎임
- 게임은 여러 단계로 구성되며, 각 단계 별로 배경 이미지와 난이도가 달라짐
- 50초 안에 2000 점을 얻어야 다음 스테이지로 넘어갈 수 있으며, 그렇지 않으면 b 버튼을 눌러 해당 스테이지를 retry 해야함
- 'HOLD' 화살표의 경우, 화살표의 사각형 꼬리가 완전히 지나갈 때까지 조이스틱을 해당 방향으로 유지하고 'A' 버튼을 눌러야 함

## 설치 및 설정

- Python 및 필요한 라이브러리 설치
  - RPi SPI 활성화 설정

    RPi 터미널에서 다음의 코드 실행
    ```
    sudo raspi-config
    Interface .. -> SPI -> Enable
    ```
  - 필요한 라이브러리 설치
    ```
    sudo pip3 install adafruit-circuitpython-rgb-display
    
    sudo apt-get install fonts-dejavu
    ```
    그 이외의 라이브러리도 필요에 따라 설치

- git clone 후 게임 스크립트를 실행
  ```
  python3 game.py
  ```

## 주의사항

1. `Adafruit 1.3" Color TFT Bonnet`의 Raspberry Pi용 LCD에 문제가 있어, GUI 디스플레이용으로 VNC와 `tk` 라이브러리를 사용합니다.
   - 조이스틱 및 버튼 기능은 여전히 Adafruit 모듈을 사용

2. 현재 과제 제출 기한으로 인해, 코드는 한 파일에 합쳐져 있습니다.
    - 곧 파일을 나누어 모듈화 및 최적화할 예정
