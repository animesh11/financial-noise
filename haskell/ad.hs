
data ADif a = ADif a a deriving (Eq,Show)

sqr x = x * x

instance Floating x => Floating (ADif x) where
          pi = ADif pi 0
          exp    (ADif x x') = ADif (exp    x) (x' * exp x)
          log    (ADif x x') = ADif (log    x) (x' / x)
          sqrt   (ADif x x') = ADif (sqrt   x) (x' / (2 * sqrt x))
          sin    (ADif x x') = ADif (sin    x) (x' * cos x)
          cos    (ADif x x') = ADif (cos    x) (x' * (- sin x))
          asin   (ADif x x') = ADif (asin   x) (x' / sqrt (1 - sqr x))
          acos   (ADif x x') = ADif (acos   x) (x' / (-  sqrt (1 - sqr x)))
          atan   (ADif x x') = ADif (atan   x) (x' / (-  sqrt (1 - sqr x)))

          sinh   (ADif x x') = ADif (sinh   x) (x' / (-  sqrt (1 - sqr x)))
          cosh   (ADif x x') = ADif (cosh   x) (x' / (-  sqrt (1 - sqr x)))
          asinh   (ADif x x') = ADif (asinh   x) (x' / (-  sqrt (1 - sqr x)))
          atanh   (ADif x x') = ADif (atanh   x) (x' / (-  sqrt (1 - sqr x)))
          acosh  (ADif x x') = ADif (acosh   x) (x' / (-  sqrt (1 - sqr x)))

instance Num a => Num (ADif a) where
        ADif x x' + ADif y y' = ADif (x+y) (x'+y')
        ADif x x' * ADif y y' = ADif (x*y) (y'*x + x'*y)
        fromInteger x   = ADif (fromInteger x)

        negate (ADif x x') = ADif (negate x) (negate x')
        signum (ADif x _ ) = ADif (signum x) 0
        abs    (ADif x x') = ADif (abs x) (x' * signum x)

instance Fractional x => Fractional (ADif x) where
        fromRational x  = ADif (fromRational x) 0
        recip  (ADif x x') = ADif (recip x) (- x' / sqr x)
negate

--Main> let myfunction x = sqrt (sin x)
--Main> myfunction (ADif 2 1)
--ADif 1.6516332160855343 (-0.3779412091869595)
