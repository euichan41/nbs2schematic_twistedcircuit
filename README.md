# nbs2schematic
converts .nbs file from Open Noteblock Studio to .litematic file.

This program converts .nbs file to .litematic file.

It converts 32 notes of 20tick/s .nbs file into 8-block-long circuit, which is twice as compressed as my previous circuit(nbs2schematic).

![image](https://user-images.githubusercontent.com/98069399/219400020-6dca43b3-ec22-4375-9dd8-2ac9bbc9c58a.png)

https://youtu.be/ip4ko1sQdt4


Before you use this program, you must prepare for .nbs files which has maximum 6 notes at the same tick, since this circuit can only play 6 notes at a time.

Therefore if your .nbs song plays more than 6 notes at a time, you must split up the .nbs file into smaller files that plays less than 6 notes at a time.



You can execute this program with nbs2schematic_twistedcircuit.exe file.

Plus, there's some .nbs example files in nbs_example folder if you need.



////

노트블럭 스튜디오로 만든 nbs 파일을 .litematic 파일로 변환해 줄 수 있는 프로그램임.



노트블럭 스튜디오에서 20tick/s 템포 기준으로 32개 노트 당 8블록 길이의 회로로 변환해줌. 이전 회로(nbs2schematic)보다 2배 더 압축된 길이임.



프로그램을 쓰기 전에, 이 회로는 동시에 6개의 노트까지만 연주할 수 있어서, 같은 틱에서 6개 이하의 노트만 있는 .nbs 파일을 준비해야 함.

만약 회로로 만들고 싶은 .nbs 노래가 한번에 6개를 넘는 노트를 연주한다면, 각각 6개 이하의 노트만 동시에 연주하도록 .nbs 파일을 나눠서 준비해야 됨



nbs2schematic_twistedcircuit.exe 파일을 더블클릭해서 프로그램을 실행할 수 있음.

nbs_example 폴더에 예시로 써볼 수 있는 .nbs 파일들을 넣어 놨음 필요하면 쓰셈.
