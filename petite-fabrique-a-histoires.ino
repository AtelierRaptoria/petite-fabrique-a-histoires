/*
 *  La petite fabrique à histoires
 *  Génération d'histoires très courtes affichées sur une écran relié à une Arduino
 *
 *  Dépôt Gitlab : https://gitlab.com/AtelierRaptoria/petite-fabrique-a-histoires
 *
 *  Matériel :
 *  - 1 carte Arduino
 *  - 1 breadboard
 *  - 1 écran LCD
 *  - 1 potentiomère
 *  - 1 bouton poussoir
 *  - 1 résistance 10kΩ
 *  - 1 résistance 220Ω
 *  - câbles
 *
 *  Installation des dépendances Python :
 *  pip install -r requirements.txt
 *
 *  Usage :
 *  1. Câbler vote Arduino comme indiqué sur le schéma
 *  2. Compiler et téléverser le script petite-fabrique-a-histoires.ino sur votre Arduino
 *  3. Lancer le script histoires.py --port <port de votre Arduino>
 *  4. Appuyer sur le bouton poussoir
 *  5. Lire les histoires 😁
*/

// Bibliothèques
// =============================================================================

#include <LiquidCrystal.h>


// Variables
// =============================================================================

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
int buttonPin = 8;
int poussoir = 0;


// Moulinettes
// =============================================================================

void setup() {
    Serial.begin(9600);
    pinMode(buttonPin, INPUT);
    lcd.begin(16, 1);
}

void loop() {
    lcd.setCursor(0, 1);
    poussoir = digitalRead(buttonPin);

    if(poussoir == HIGH) {
        Serial.write(1);
        defilementTexte(Serial.readString());
        delay(2000);
    } else {
        Serial.write(0);
        lcd.clear();
    }

    delay(100);
}

void defilementTexte(String texte) {
    int longueur = texte.length();
    int lcdWidth = 16;

    if(longueur < lcdWidth) {
        lcd.print(texte);
    } else {
        int idx;
        for(idx = 0; idx < lcdWidth; idx++) {
            lcd.print(texte[idx]);
        }

        delay(1000);

        while(idx < longueur) {
            lcd.scrollDisplayLeft();
            lcd.print(texte[idx]);
            idx = idx + 1;
            delay(100);
        }
    }
}
