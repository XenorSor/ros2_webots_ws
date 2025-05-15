Kezdés:
  Le kell klónozni a gites fájlt a git clone kóddal, de ehhez publikusnak kell lennie.

  Le kell szedni a webots-ot: wget github.com/cyberbotics/webots/releases/download/R2025a/webots_2025a_amd64.deb

  Ezután ezt a .deb fájlt egy: sudo apt install ./webots_2025a_amd64.deb -> által megkapjuk a webots-ot az /usr/local/webots mappába

  Kelleni fog egy: pip install pynput, ha esetleg nem lenne

  Továbbá kell egy a következő csomag: sudo apt-get install ros-humble-webots-ros2

  Windows wsl esetén egy fájlt át kell írni: \\wsl.localhost\Ubuntu-22.04\opt\ros\humble\local\lib\python3.10\dist-packages\webots_ros2_driver\utils.py itt a def is_wsl(): függvénynél azt kell írni, hogy: return False

Projektben kezdetek:
  kell a terminálba a következő kódok:
    colcon build ||
    source install/setup.bash ||
    export WEBOTS_HOME=/usr/local/webots

Projekt struktúrája:
  src mappán belül a következők állnak:
    launch - programok futtásáért felelős ||
    resource - urdf fájlokat tartalmaz, amely kommunikál a szimulátor és kód között ||
    ros2_webots - itt találhatóak a node-ok, kontrollerek ||
    worlds - itt található a szimulációs környezetek ||

Launcherek:
  3 launcher van

  1. car_first_launch.py:
     ez elindítja a webots-ot és egy robotot
     majd a webots-ot hozzá kötjük .urdf fájllal egy plugin/controllerhez
     ez a launcher teleoperációt végez el, ha a webots konzolba leütjük a "w", "a", "s", "d", " ", felfele nyilat, akkor a robot elindul
      ![kép](https://github.com/user-attachments/assets/eec8ddf3-cb43-419c-a51b-4abe16d9e095)
      kódja:
     ![kép](https://github.com/user-attachments/assets/3d23ef7f-9b82-45e6-9a42-f37c3a2926e7)
      webots változó indítja el szimulációt a megfelelő környezettel ||
      my_robot_driver változó által képesek vagyunk a robot irányítani egy kontrollerrel, ami össze van kötve egy urdf-vel és a robot újrahívása engedélyezve van
  
  2. car_second_launch.py:
      ez elindítja a webots-ot és egy olyan robot amely rendelkezik szenzorokkal
      ez automatikusan mozgó robot, amely valamelyest képes akadályokat kikerülni
      ![kép](https://github.com/user-attachments/assets/4228fbaf-d514-4bbc-85fd-1b861d61f8f8)

    
  3. epock_launch.py:
      ez elindítja a webots-ot, amely egy labirintus és egy epock robotot,
      a robot automatikusan a falat követve közlekedik
      ![kép](https://github.com/user-attachments/assets/5a87e668-c741-421f-a270-52286030caae)

URDF-ek:
  ![kép](https://github.com/user-attachments/assets/41eaea09-c592-4231-a95c-65ca5d3fe004)
  itt építjük ki a kapcsolatot a szimuláció és kontroller között ||
  plugin a kontrollerünk ||
  a device pedig a szenzorunk

Kontroller:
  ![kép](https://github.com/user-attachments/assets/c427e290-d7f9-47e4-bd43-d80e3b71069d)
  Így nézz ki egy szimpla kontroller
  kell neki egy init, amely rendelkezik 3 paraméterrel, amely szükséges egy webots kontrollernek: self, webots_node, properties;
  webots_node tárolja a robotot ||
  getDevice által képesek vagyunk a robot egyes elemeit kivenni egy változóba ||
  rclpy által kell egy node-ot létrehozni webots kontroller esetén ||
  a setVelocity beállítja a motor sebbeségét ||
  step függvény alapján működnek a kontrollerek ez alapján vagyunk képesek irányítani a robotot, ahol a kezdésnek kötelező egy ilyet adni: rclpy.spin_once(self.node, timeout_sec=0)

  3 kontrollerünk van:
    1. car_driver:
        itt mondható meg, hogy a robot merre, mennyire haladjon
    2. epuck:
        itt mondjuk meg az epuck robotnak, hogy hogyan kövesse a falakat
    3. teleop:
        itt állítjuk be, hogy a robot teleoperáció alapján is tudjon mozogni

Node:
  van egy obstacle_avoider node-unk, amely a robot szenzorai alapján dönt arról, hogy merre forogjon a robot

Worlds:
  itt található a szimulátorok környezete, kód formátumban
  működésükhöz szükséges internet kapcsolat
