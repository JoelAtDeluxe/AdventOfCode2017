# Whatever


## Code flow

``` bash
Inst  #  Flow
======+=====================
  0   #               set b 65
  1   #               set c b
  2   #               jnz a 2
  3   #               jnz 1 5
  4   #               mul b 100
  5   #               sub b -100000
  6   #               set c b
  7   #               sub c -17000
  8   #  +----------> set f 1
  9   #  |            set d 2
 10   #  |  +-------> set e 2
 11   #  |  |  +----> set g d
 12   #  |  |  |      mul g e
 13   #  |  |  |      sub g b
 14   #  |  |  |  +-< jnz g 2
 15   #  |  |  |  |   set f 0
 16   #  |  |  |  +-> sub e -1
 17   #  |  |  |      set g e
 18   #  |  |  |      sub g b
 19   #  |  |  +----< jnz g -8
 20   #  |  |         sub d -1
 21   #  |  |         set g d
 22   #  |  |         sub g b
 23   #  |  +-------< jnz g -13
 24   #  |        +-< jnz f 2
 25   #  |        |   sub h -1
 26   #  |        +-> set g b
 27   #  |            sub g c
 28   #  |        +-< jnz g 2
 29   #  |     *<<|<< jnz 1 3 ***
 30   #  |     |  +-> sub b -17
 31   #  +-----|----< jnz 1 -23
 **   #        |
 **   #        ---> Exit
 ```



### Real code 

```java
// literal (but sub X - ɑ is now X + ɑ, and some jnz have been turned into if/do-while s)
public static void doSomething() {
  // preamble -- presumably user-specific customization
  var a = 0, b = 0, c = 0, d = 0, e = 0, f = 0, g = 0, h = 0; // starting cond

  a = 1;  // starting condition for part 2
  b = 65;  // 0
  c = b;   // 1
  if (a != 0) { //2, 3 (2 if true, 3 if false)
    b *= 100;    // 4
    b += 100000; // 5
    c = b;       // 6
    c += 17000;  // 7
  }

  // Algorithm
  do {
    f = 1;              //  8
    d = 2;              //  9
    do {
      e = 2;            // 10
      do {
        g = d;          // 11
        g *= e;         // 12
        g -= b;         // 13
        if g == 0 {     // 14
          f = 0;        // 15
        }
        e += 1;         // 16
        g = e;          // 17
        g -= b;         // 18
      } while (g != 0); // 19
      d += 1            // 20
      g = d;            // 21
      g -= b;           // 22
    } while (g != 0);   // 23

    if (f == 0) {       // 24
      h += 1;           // 25
    }
    g = b;              // 26
    g -= c;             // 27
    if (g == 0) {       // 28
      return;           // 29  (this jumps out of the script, so it's basically a return)
    }
    b += 17;            // 30
  }
  while (true);         // 31
}
```

```java
// slightly tweaked
public static void doSometing() {  // count composite numbers between b and c?
  // simplify the starting condition -- assumes running part 2.
  var a = 1;
  var b = (65 * 1000) + 100000;
  var c = b + 17000;
  
  var g = 0;
  var h = 0;
  do {
    var f = 1;            // 8
    var d = 2;            // 9

    // This loop is basically checking if this number is prime.
    // If it's prime, f = 1, otherwise, f = 0
    do {
      var e = 2;          // 10
      do {
        g = (d * e) - b;  // 11, 12, 13
                          // This is basically just checking if b = e * d
                          // ==> suppose g = 0  ;; then that's: 0 = (d * e) - b => b = d*e
        if (g == 0) {     // 14
          f = 0;          // 15
          break;          // OPTIMIZATION: The only thing that persists beyond this are g, d, f
                          // g seems to be temporary storage
                          // d is stable inside so doesn't matter
                          // f is the onlything relevant here -- it's changed, so we can leave
                          // Actually, we can break out of the outer loop
        }
        e++;              // 16
        g = e - b;        // 17, 18
      }
      while (g != 0);     // 19

      d++;                // 20
      g = d - b;          // 21, 22
    } while (g != 0);     // 23

    if f == 0 {           // 24
      h++;                // 25
    }
    g = b - c;            // 26, 27
    if (g == 0) {         // 28
      Systme.out.println("Value of h is: " + h);
      return;             // 29
    }
    b += 17;              // 30
  } while( true );        // 31
}
```

```java
// tweaked, logic unchanged (except for typos -- might have an off-by-one error on the outr loop)
public static void doSometing() {
  var compositecount = 0;
  for (int b = 106500; b <= c; b += 17) { // starting cond + inst 30, 26, 27, 28, 29
    var isPrime = true;                 // 8  //former f = 1

    // basically: if b can be expressed as a product of two numbers
    // the loop iterations are pretty silly here. Optimized would need a sqrt instruction
    for( int d = 2; d < b; d++ ) {   //  9, 20, 21, 22, 23
      for ( int e = 2; e < b; e++) { // 10, 16, 17, 18, 19
        if ((d * e) == b) {          // 14  11, 12, 13
          isPrime = false;           // 15  // former f = 0;
        }
      }
    }

    if (!isPrime) { //24 //former f == 0
      compositecount++;      //25 //formerly h++
    }
  }
}
```

```py
# optimized version of is_prime
def is_prime(LIMIT):
  for i in range(LIMIT):
    res = LIMIT % i
    if res == 0:
      f = 0
      break
```

``` sh

# As script

set counter 2
set exit_cond b
set step -1
jnz 1 2
sub counter step
# Check exit
set exit_cond_check exit_cond
sub exit_cond_check counter
jnz exit_cond_check 2
jnz 1 7
# logic
set testLimit b
mod testLimit counter
jnz testLimit 3
set f 0  # update that we found something
jnz 1 2  # exit
jnz 1 -10

# Diagrammed

 INST    # Flow
=========+===================
 n +  1  #             set counter 2
 n +  2  #             set exit_cond b
 n +  3  #             set step -1  # we can lose this step
 n +  4  #        +--- jnz 1 2
 n +  5  #  +---- | -> sub counter step
 n +  6  #  |     +--> set exit_cond_check exit_cond
 n +  7  #  |          sub exit_cond_check counter
 n +  8  #  |     +--- jnz exit_cond_check 2
 n +  9  #  | +-- | -- jnz 1 7
 n + 10  #  | |   +--> set testLimit b
 n + 11  #  | |        mod testLimit counter
 n + 12  #  | |   +--- jnz testLimit 3
 n + 13  #  | |   |    set f 0
 n + 14  #  | |<- | -- jnz 1 2
 n + 15  #  +---< +--> jnz 1 -10
   **    #    |
   **    #    +------> Exit


# Sanitized
# New size: 14
# original: 23-10 + 1 = 14
set i 2
set x b
jnz 1 2
sub i -1
set m x
sub m i
jnz m 2
jnz 1 7
set l b
mod l i
jnz l 3
set f 0
jnz 1 2
jnz 1 -10

```

## Code flow constructs

### For loop (i = 0; i < x; i++)

```sh
# Initialize
set counter 1
set exit_cond 2
set step 3
set exit_cond_check exit_cond
jnz 1 2# bypass first step
sub counter step # add step
# Check exit
sub exit_cond_check counter
jnz exit_cond_check (logic-block)
jnz 1 (exit-loop)
# logic
jnz 1 (exit_cond_check step)

# diagramed

Inst   #  Flow
=======+=====================
  0    #             set counter 1
  1    #             set exit_cond 2
  2    #             set step 3
  3    #             set exit_cond_check exit_cond
  4    #        +--- jnz 1 2
  5    #  +---- | -> sub counter step
  6    #  |     +--> sub exit_cond_check counter
  7    #  |     +--- jnz exit_cond_check (logic-block)
  8    #  |  +- | -- jnz 1 (exit-loop)
  9+   #  |  |  +--> (Logic goes here)
n + 10 #  +- | ----- jnz 1 (exit_cond_check step)
 **    #     |
 **    #     +-----> Exit


```

