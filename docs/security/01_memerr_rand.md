# Memory Errors: Exploits and Defenses

## Quick Description (QD)

This chapter covers memory exploits and their defenses. Today, compilers and programming languages are designed to be safe against memory errors. Nevertheless, bad development practices can open ways for attackers to perform their attacks.

### Memory Layout of a Process

A process keeps its data in several memory regions: the program code, global data, the heap, and the stack (which holds local variables, saved registers and return addresses). Command-line arguments and environment variables are placed at the top.

Here is a view of the memory layout of an application.

| High memory | - |
|---|---|
| argv, env   | command-line args and environment |
| stack       | generally grows downwards |
| heap        | generally grows upwards |
| bss         | uninitialized global data |
| data        | initialized global data |
| text        | read-only program code |
| __Low memory__  | _-_ |

In code example:

```c
int a = 1; // Data
int b; // BSS

// Text
int main(int argc, char **argv) /* ptr to argv */
{
    int *c; // Stack (local variable)
    c = (int *)malloc(5 * sizeof(int)); // Heap (dynamic allocation)
}
```

### Call Stack (Activation Record / Stack Frame)

An activation record is created for each procedure.

Structure of stack frame:

| High memory (the stack grows downward) |
|-------------|
| Actual parameters |
| Return value |
| Return address |
| Saved BP (base pointer / frame pointer) |
| Local variables |
| Temporary variables |

### Stack Access

Most items on the stack are accessed relative to __Base Pointer__.
Typically they can get accessed using a hard-coded offset into binary.
__Stack Pointer (SP)__ moves on push/pop.
However, base pointer only moves on function call/return.

#### Caller to Callee

When a caller calls a callee, it first pushes all params onto the stack in reverse order, then the `call` instruction pushes the return address. Then the callee performs the following tasks (the function prologue) in order:

1. Push base pointer onto stack. (save previous function base pointer)
2. Copy stack pointer to base pointer.
3. Reserve stack space for local vars.

#### Callee to Caller

After the callee is done, it performs these tasks in order:

1. Store return value in `eax` or `rax`.
2. Reset stack to pre-call state (the function epilogue). Destroys current stack frame, and restores caller's frame (`leave`).
3. Return control back to the caller (`ret` pops the return address).

### Stack Smashing

Stack smashing is an attack that exploits a stack buffer overflow. Typically, a program writes more data to a buffer than it is capable of holding, so the data overwrites adjacent memory, including the saved base pointer and the return address. An attacker can use this to hijack the control flow, for example by pointing the return address to injected code.

#### Defense 1: Non-executable Data (DEP, NX, W XOR X)

The first defense solution is non-executable data.
Prevent execution of data to block code execution.
It counters direct code injection.
However, to pass this defense, two attacks are used, __Return to libc__ and __Return-oriented programming (ROP)__.

#### Evasion 1.1: Return to Libc

Use code that already is in process memory.
Exploitable functions exist in __libc__, the low-level system library that is part of every program. Examples:

- `system`
- `execve`

The attacker needs to control the arguments to this function. Since the attacker controls the stack contents, and the function reads its arguments from the stack, this is possible.

A typical attack runs `/bin/sh` by overwriting the return address with the address of `system` and placing a pointer to the string `"/bin/sh"` as its argument on the stack.

#### Evasion 1.2: Return-Oriented Programming (ROP)

In this technique, an attacker gains control of the call stack (stack pointer) to hijack program control flow and then executes carefully chosen machine instruction sequences that are already present in the machine's memory, called __gadgets__.

To put it in simple words, this attack involves using the stack pointer as the attacker's program counter. The attacker's "program" is a chain of gadget addresses (and data) placed on the stack; each gadget ends with a `ret` instruction, which transfers control to the next gadget. The victim's existing code is used as the building blocks.

#### Defense 2: Stack Canary

To detect stack smashing, the callee stores a __canary__ value on the stack, between the local buffers and the saved base pointer and return address. The value is stored on function entry and checked before return. If the canary is dead (changed), the program is aborted, which turns a __control-flow hijack__ into a __DoS (denial of service)__.

#### Canary Defense Issues

1. Fixed values for canary can be detected by attackers.
2. Random canary is better, but the attack can rely on a vulnerability that reveals canary value.
3. XOR canary: the canary is XORed with the return address (or other control data), so that overwriting them without knowing the canary is detected. However, it breaks compatibility with stack tracing and debuggers.

#### ProPolice

ProPolice (also known as SSP, the stack-smashing protector, used by GCC) is a contemporary canary-based defense. It rearranges the stack layout to make the stated attacks harder.

It includes the following steps:

1. Create a random canary value at process start time.
2. Protect return address and base pointer by locating canary below saved base pointer.
3. Reorder local variables so that simple variables occur after variables subject to overflow.

The stack structure after applying these steps becomes:

| High memory (the stack grows downward) |
|-------------|
| Old stack frame |
| parameter #N |
| ... |
| parameter #1 |
| RA |
| Saved BP |
| Canary |
| Array-type local variables |
| Non-array type local variables |

#### Bypassing Canaries

There are some methods to bypass the canary. In other words, the attacker can still perform attacks without killing the canary.

- Indirect (aka double pointer) overwrite vulnerability. If the code has a pointer on the stack that the attacker can overflow into, the attacker can first overwrite that pointer with the address of the return address, and then make the program write through it. This writes directly to the return address and jumps over the canary.
- Brute-force attacks in which attackers try every possible value for the canary until they succeed. This is practical when a server restarts workers with the same canary (e.g., by `fork`).
- Partial overwrite in which attackers guess the canary one byte at a time.
- Information leaks, which exploit a memory error that allows reading arbitrary memory locations. A common example is the __format string__ attack (see below).

#### Other Defenses for Return Address

- __Shadow Stack__: In this method, we store a copy of the return address in a separate, protected place, and compare it on return.
- __Safe Stack__: In this method, the compiler moves arrays and any variable whose address is taken off the main stack (see the notes below). It is already implemented in compilers like LLVM/Clang.

### Beyond Stack Smashing

In this section, we take a look at attacks on other parts of the memory, since stack is not the only memory that is being used by applications.

#### Overflows in Heap-allocated Buffers

For a buffer allocated on the heap, there is no return address nearby. So, attackers should overwrite other code pointers like heap metadata or a function pointer.

#### Heap Metadata Overwrite

A heap buffer overflow, or the use of a pointer that has not been properly initialized or has already been freed, can overwrite critical heap metadata. This can corrupt the allocator's view of the heap, causing unpredictable behavior, which is, of course, predictable by the attacker.

It provides a primitive to write an attacker chosen value to an attacker chosen location (e.g., when the allocator unlinks a block from a doubly linked free list). Some systematic solutions are __heap canaries__ and __separating metadata from data__.

#### Format-string Vulnerabilities

This vulnerability appears in code that passes attacker-controlled data as the format string, such as `printf(s)` with `s` provided by the attacker. `printf` then blindly interprets the stack contents as the arguments that the format string asks for. Normally `printf` only reads memory, but the `%n` conversion allows a memory write: it writes the number of characters printed so far.

According to the `printf(3)` man page, here is what `%n` does:

- The number of characters written so far is stored into the integer indicated by the `int *` (or variant) pointer argument. No argument is converted.

So the primitive is to write the number of characters printed to an attacker-chosen location. Below are some format parameters which can be used and their consequences:

- `%x` Read data from the stack (as hexadecimal)
- `%s` Read character strings from the process' memory (the argument is treated as a pointer)
- `%p` Print a stack value as a pointer
- `%n` Write an integer to a location in the process' memory

#### Integer Overflows

Integer overflows can take multiple forms:

- variables of different widths.
- variables of different signs.
- arithmetic overflows.

These can subvert bounds and size checks. For example, a check that passes for a bad value:

```c
int sz = ...;
if (sz < n) memcpy(buf, src, sz); // a negative sz passes the check, then becomes a huge size_t in memcpy
```

#### Use-after-free Vulnerabilities

Most past attacks were based on out-of-bounds writes. But recently, attention has shifted to __use-after-free__ data accessed through dangling pointers. In a typical attack, the victim uses a dangling pointer to access critical data, but the block has already been freed and reallocated for processing the attacker's input.

A __dangling pointer__ is a variable in a programming language that points to a memory location that is no longer valid or has been deallocated.

### Systematic Study of Memory Errors

In this section, we take a systematic look at memory errors. The idea is to get a general view of memory errors.

#### Memory Errors

A memory error happens when an object accessed using a pointer expression is different from the one intended by the programmer. There are two types of memory errors:

- __Spatial error__: out-of-bounds access, access using a corrupted pointer, uninitialized pointer access
- __Temporal error__: access to objects that have been freed, dangling pointers, applicable to stack and heap allocated data

Most attacks used to be based on spatial errors, but today, temporal errors have become very important.

- __double free__
- __use-after-free__

Typical attacks involve an out-of-bounds write to corrupt a pointer. This means that most attacks rely on multiple memory errors.

- Stack Smashing: out-of-bounds write + use of a corrupted pointer as return address
- Heap Overflow: out-of-bounds write + corrupted pointer for write and corrupted pointer as target

#### Overview of Memory Error Defenses

Memory error defenses can divide into two categories:

- __Prevent memory corruption__
- __Disrupt exploits__ (guarding solutions)

#### Prevent Memory Corruption

Detect and stop memory corruption before it happens. It targets spatial errors, where we detect access past the end of valid objects. All spatial errors can be detected by recognizing pointer arithmetic that crosses object boundaries.

#### Disrupt Exploits

Corruption is not stopped always. Therefore, __guarding solutions__ is the answer:

- Disrupt __corruption__
- Disrupt __take-overs__ (Randomization-based defenses)
- Disrupt __payload execution__

#### Disrupt Corruption

Protect attractive targets against common ways to corrupt them.

#### Disrupt Take-overs (Control-flow Hijack)

A key issue for an attack is using their controlled inputs to induce errors with predictable effects. Their approach is to exploit software bugs to overwrite critical data:

- __Relative address attacks__ (RA)
- __Absolute address attacks__ (AA)
- RA + AA attacks

In order to disrupt them, we use __Benign diversity__:

- __Preserve functional behavior__: on benign inputs, diversified program behaves exactly like the original program.
- __Randomize attack behavior__: on inputs that exercise a bug, diversified program behaves differently from the original program.

#### Automated Introduction of Diversity

The idea is to use transformations that preserve program semantics. The focus is on programming language semantics, to randomize implementation aspects that aren't specified in the programming language. Examples:

- __Address Space Randomization (ASR)__: randomize memory locations of code or data objects.
- __Data Space Randomization (DSR)__: randomize low-level representation of data objects.
- __Instruction Set Randomization (ISR)__: randomize interpretation of low-level code.

Without using randomization, memory errors corrupt memory in a predictable way. This means the attacker knows the exact data item that is corrupted (which RAR and DSR make unpredictable), and the correct value to use for corruption (which AAR and DSR make unpredictable).

#### Absolute Address Randomization (AAR/ASLR)

Randomize base address of data and code.

- data: stack, heap, static memory
- code: libraries and executable regions

Limits:

- Incomplete implementations
- Relative address data-only attacks
- Information leakage attacks
- Brute-force in space domain using NOP padding or __Heap spray__

Heap spray exploits compromise an application by placing shellcode onto the heap then executing it through various vectors.

#### Relative Address Randomization (RAR)

Randomize distance between static objects. This is done at compile time. Randomize distance between stack objects. Since the entropy is limited if the number of variables is small, better option is __safe stack__. Heap allocations can be randomized without help from compilers.

#### Fine-grained Code Randomization (RAR for Code)

To make __ROP (return oriented programming)__ infeasible:

- Permute order of functions
- Randomly rearrange instructions within a function

Benefits of RAR:

- Defeats the overwrite step, as well the step that uses the overwritten pointer value.
- Provides higher entropy.
- Unlike AAR, a single information leak is insufficient to derandomize everything.

#### Data Space Randomization (DSR)

The basic idea is to randomize data representation. We XOR each data object with a distinct random mask. Therefore, effect of data corruption becomes non-deterministic. Unlike AAR, DSR protects all data, not just pointers. Effective against relative address as well as absolute address attacks. It also has a large entropy.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

### Notes and Comments

- In memory exploits, sometimes the exact address of the injected code is uncertain. To deal with it, the attacker prepends a `NOP-sled` to the code. A `NOP` instruction does nothing and falls through to the next one, so jumping anywhere into the sled slides execution down to the real payload.
- In a callee to caller operation, the local variables of caller will be referenced relative to `BP` (base pointer). Therefore, if the attacker wants to control the caller variables, it should change the BP to point to a different location. Moreover, the attacker can set the value of these variables relative to the new location of `BP`.
- One good solution to prevent Stack Smashing attacks is to use a __Safe Stack__. The compiler creates two stacks: (i) a safe stack in which all of the control data and simple variables are stored, and (ii) a second stack that stores arrays, or more generally, any variable whose address is taken.
- In Heap memory defense using a Canary value, the value should be the first field in the heap block. It should have a random value that is unpredictable. And, it's value should be checked before any of the heap block fields are accessed.
- If you can somehow inject code, it can figure out the randomness. In other words, randomization does not provide much protection against malicious code; but it can protect benign programs from vulnerabilities such as buffer overflow.
- `GOT` is a table of function pointers that is used to dispatch calls to shared libraries. Typically, heap overflow attacks are used to overwrite GOT entries, say, the entry corresponding to the read system call.

## Examples (e.g.,)

_Nothing here yet._

## References

- [Aleph One: Smashing the Stack for Fun and Profit (Phrack 49)](http://phrack.org/issues/49/14.html)
- [Cowan et al.: StackGuard, Automatic Adaptive Detection and Prevention of Buffer-Overflow Attacks (USENIX Security 1998)](https://www.usenix.org/legacy/publications/library/proceedings/sec98/full_papers/cowan/cowan.pdf)
- [Shacham: The Geometry of Innocent Flesh on the Bone, return-into-libc without function calls (ROP)](https://hovav.net/ucsd/dist/rop.pdf)
- [Clang SafeStack](https://clang.llvm.org/docs/SafeStack.html)
- [printf(3)](https://man7.org/linux/man-pages/man3/printf.3.html)
- [OWASP: Format string attack](https://owasp.org/www-community/attacks/Format_string_attack)
- [Address space layout randomization (Wikipedia)](https://en.wikipedia.org/wiki/Address_space_layout_randomization)
