## LazyHDL v0.1 Syntax Guide
Hi my name is Blake Lazarine and I am making a new HDL

It is heavily inspired by Verilog, but simplifies parts that confuse me.
Also, I don't know how to make a compiler and this syntax is easier for me to parse with regex.
It supports the standard input, output, and intermediary wire connections as well as registers.

Not yet included but in progress:

* Variable bit count
* Nested modules
* multi-line equations
* multi-line comments
* declaring multiple variables/wires in one line
* support for non-base-10 numbers

an overview of syntax goes as follows:

Declare an Input:
```
input name[bit_width]
ex.
input hello[8]
```
Simple enough, right?
Currently, the bit_width has no meaning, but will soon

As you can see, no semicolons are needed, which I kind of like.
This might change in future versions for the sake of multi-line statements.
But that is a question for future me.

Declare an Output:
```
output name[bit_width]
ex.
output goodbye[1]
```
Seems familiar, huh?

We want our outputs to mean something, so we need to assign a value.
Verilog's precedent is to have inputs and outputs declared at the top of the module.
I like this, but it means you need to assign the output values later in the code.
Doing this is pretty straightforward:
```
assign name = expression
ex.
assign goodbye = 3 + in
```

Declare an intermediary wire:
```
wire name[bit_width] = expression
ex.
wire w[32] = in + other_wire
```
Whenever you declare an intermediary wire, you need to set the expression right then and there.
This might change later, but for now it makes my life easier and also prevents simulated oscillation.
By that I mean, you can't have the 'output' of an intermediary wire be used as input for the same wire.
Think of it like in Minecraft when you have a redstone torch that disables itself.
This creates rapid oscillation until the torch burns out.
I do not want my redstone torches to burn out, so I make it impossible to use multiple wires to create this oscillation.
I do have it possible to directly feed a variable into its own equation, but I can fix that without too much hastle.

'But Blake', you might be asking, 'Don't sequential systems feed into themselves to create functionality?'

Excellent question, that's what registers are for.
Registers only update their value on positive or negative edges of signal change.
This avoids hardware oscillation, which is good.

You can declare registers in LazyHDL as such:
```
reg name[bit_width] (initial_value, posedge/negedge other_name)
assign name = expression

OR
reg name[bit_width] (initial_value, posedge/negedge other_name) = expression

ex.
reg hey_there[32] (0, posedge clk) = some_in & some_wire
```

In this example, the register of name 'hey_there' will be initialized to a value of 0.
Whenever the input or intermediary wire called 'clk' goes from 0 to 1, 
the value stored in 'hey_there' will be recalculated based on the defined expression
 