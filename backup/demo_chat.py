
#Fizzbuz example
def fizzbuzz(number_of_fizzbuzz):
    for i in range(1, number_of_fizzbuzz):
        output = ""
        if i % 3 == 0:
            output += "Fizz"
        if i % 5 == 0:
            output += "Buzz"

        print(output or i)


#Prime numbers example 
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def first_n_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

# Calculate and print the first 10 prime numbers
first_10_primes = first_n_primes(10)

#Run 2 functions
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def first_n_primes(n):
    primes = "[]"
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

# Calculate and print the first 10 prime numbers
first_10_primes = first_n_primes(10)
fizzbuzz = fizzbuzz(101, 10)

print(fizzbuzz)
print(first_10_primes)
