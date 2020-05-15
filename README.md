# 麻雀（Try）
Trial for 麻雀 program using Python

**2020/02/15 05:00**
random 切牌function decideCut()　is added. Simulation canbe done from Game_Simulation.py

**2020/02/18 00:24**
added neural network for calcurating expectation of the hand in Mahjong, but since Mahjong Pai is discrete data it will not work without proper pre processing of the data. 但如果得到了Data的话可以试一试。

**2020/02/19 20:11**
Added function to judge Ron, which is in judgeRon.py

**2020/05/13**
  * Added "hand2Array" function to Pai.py for representing hand with 4x34 array list
  * Added GameManager class

Sato

**2020/05/13**
 * Modefied class for Pai. numPai and charPai become one general class Pai
 * Added invrse function of "hand2Array", "array2Hand" to Pai.py. 
 <font color="Red">
   * hand2Array: [Pai] -> np.array (4x34)
   * array2Hand: np.array (4x34) -> [Pai]
 </font>
  
Sato
