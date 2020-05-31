## Bayes' Nets

- [Bayes' Rule](#bayes'-rule)
- [Independence](#independence)
- [Conditional Independence](#conditional-independence)
- [Bayes' Nets Representation](#bayes'-nets-representation)



[Back](../README.md)

---

### Bayes' Rule

From last topic we know: $\large P(x,y)=P(x|y)P(y)=P(y|x)P(x)$

Re-arrange this equation, we get:  $\large P(x|y)=\frac{P(y|x)}{P(y)}P(x)$

**Why this is at all helpful ?**

- Let us build one conditional from its reverse
- Often one conditional is tricky but the other one is simple
- Foundation of many systems we'll see later

**Inference with Bayes' Rule**

Example: Diagnostic probability from casual probaility:

$\large P(cause|effect)=\frac{P(effect|cause)P(cause)}{P(effect)}$

---

### Independence 

Two varaibles are independent if: $\forall x,y:P(x,y)=P(x)P(y)$

This says that their joint distribution factors into a product two simpler distributions

Another form: $\forall x,y: P(x|y)=P(x)$

We write: $\large X \perp\!\!\!\perp Y$

---

### Conditional Independence

$X$ is conditionally independence of $Y$ given $Z$ 

if and only if:

$\forall x,y: P(x,y|z)=P(x|z)P(y|z)$

or, equivalently, if and only if 

$\forall x,y,z: P(x|z,y)=P(x|z)$

**Conditional Independence and the Chain Rule**

Chain rule: $P(X_1,X_2,...X_n)=P(X_1)P(X_2|X_1)P(X3|X_1,X_2)...$

Trivia decomposition:

$P(Traffic,Rain,Umbrella)=P(Rain)P(Traffic|Rain)P(Umbrella|Rain,Traffic)$

With assumption that *Umbrella​* and *Traffic​* are conditionally independent (*Umbrella* does not cause *Traffic* and vice versa when *Rain* is given, in real life *Umbrella* and *Traffic* seems to correlate just because from *Umbrella* we infer that it's likely to *Rain* and *Rain* will cause *Traffic* ):

$P(Traffic,Rain,Umbrella)=P(Rain)P(Traffic|Rain)P(Umbrella|Rain)$

---

### Bayes' Nets Representation

---

