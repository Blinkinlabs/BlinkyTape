// We want to make some hex data!


// Procedure for patching the hex file, and setting up this class:
// 1. Inspect bootloader hex file to find lowest address in use (m_freeSpaceEnd = 0x7000 - 1)
// 2. Inspect hex file to find highest address in use (m_freeSpaceStart = 0x1AD2 + 0xE)
// 3. Disassemble hex file (avr-objdump -m avr -D firmware_WS2811.cpp.hex > firmware_WS2811.cpp.S)
//     and look for this part:
//     5f8:       6d ea           ldi     r22, 0xAD       ; 173
//     5fa:       7e ed           ldi     r23, 0xDE       ; 222
//    This is where the animation class is being declared (earlier, we set the
//    data address to 0xDEAD)
// 4. Now we have to overwrite these instructions to change the size and address to point to
//    our new values. We want something like this:
//     5f8:       6Z eY           ldi     r22, 0xYZ       ; 173
//     5fa:       7X eW           ldi     r23, 0xWX       ; 222
//     Where WXYZ is the location of the data field.
//    Note: The LDI opcode looks like this:
//     1110 KKKK dddd KKKK, where K is the immediate data to load, and d is the register to load...
//     that's why everything looks really munged up.
//
//  5. Now, open up the hex file again and look for the offending line(s):
//     :1005F000C90108958EE291E06DEA7EED0E94A701A7
//     We want to change it like this:
//     :1005F000C90108958EE291E06ZEY7XEW0E94A701??
//     For our example, that becomes this (WXYZ = 1AE0):
//     :1005F000C90108958EE291E060EE7AE10E94A701??
//  6. Finally, we have to compute the checksum (the ?? bit at the end). Just add up each of the
//     hex digits, and take the 2's compliment of the result. You can do it using the os x calculator.
//     Again, for our example:
//     :1005F000C90108958EE291E060EE7AE10E94A701C0
//     Plug that back into the hex file, and we're ready to add our data structure to the end.


// Starting at offset in array data, calculate the checksum for len characters.
// Checksum is a simple 2's compliment of the addition of the data
int calculateChecksum(byte[] data, int offset, int len) {
  int sum = 0;
  for(int i = offset; i < offset + len; i++) {
    sum = (sum + data[i])&0xFF;
  }
  return ((0x100 - sum)&0xFF);
}




class Hexifier {
  int m_freeSpaceStart;  // First free memory location (end of the application program)
  int m_freeSpaceEnd;    // Last free memory location (beginning of the bootloader - 1)
  int m_maxLength;       // Maximum data size, in bytes
  
  Hexifier() {
    
    // This data taken from one hex file- need to update if that file is changed!
    m_freeSpaceStart = 0x1ABA + 0xE;
    m_freeSpaceEnd = 0x7000 - 1;
    
    m_maxLength = m_freeSpaceEnd - m_freeSpaceStart;
    
    println(m_maxLength);
  }
}
