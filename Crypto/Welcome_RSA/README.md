# Welcome RSA

>> Welcome, here is a RSA crypto challenge. Good luck

Look at the challenge script, this is what we got: 

+ We are given $N$, $e$ but also $\phi$ of the RSA Cryptosystem. (Then indeed private number $d$)
+ The ciphertext is encrypted in `RSA-CRT` way, where the plaintext is computed as:

$$
c_p \equiv m^e \pmod p \\
c_q \equiv m^e \pmod q
$$

The first thing we can say is with both $N$ and $\phi$, one can really easily to factor the number $N$. More specifically, you can got the idea from this [Mathematic Stack Exchange](https://math.stackexchange.com/questions/2087704/factoring-n-when-phin-is-given) question. For us, we use this below Sage script:

```Python 
def crack_rsa(n, phi_n):
    R.<x> = PolynomialRing(QQ)
    f = x^2 - (n + 1 - phi_n) * x + n
    return [b for b, _ in f.roots()]
```

And got the result: 

```
[147104365757691981886238610446852083772841819693796888090431035243348558951749166732911919966095528015639093479095140498246787044493026711142267958117969642510892775707277836254280575518402347244263800318277951658352705099052315213650933965287062152329328064087037860117076683589910195814549861226288772917891, 133879566549680173115010000656575599386347196254555820845731098396987569234168170667682173669730202089319438083372479965107156729576438511660256112210092621038817523549520785823861905813922287648879467800147350606041615014555319097811201748949898135983939033500537527258201074877029166631336090676510695537951]
```

The remain part is really easy. You can use Chinese Remainder Theorem to decrypt the message by solving the system of congruence: 

$$
m_p \equiv c_p^{(d \pmod{p-1})} \pmod p \\
m_q \equiv c_p^{(d \pmod{p-1})} \pmod q
$$

The solution of this system is essentially $m$ modulo $N$. The solved script is also attached :).

Flag `ASCIS{W3lc0me_t0_th3_P4rty_8597b0394054835f80ebd573a238ddbe1d86942657a59a7b6f84660d629472b5}`