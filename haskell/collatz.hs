import Data.Char
collatz :: Int -> String
collatz n
        | (n==1) = "1"
        | (n `mod` 2==0) = (show (truncate $ (fromIntegral n))) ++ "->" ++ (collatz (truncate $ (fromIntegral n)/2))
        | otherwise = (show (n))++"->" ++ collatz (3*n+1)





