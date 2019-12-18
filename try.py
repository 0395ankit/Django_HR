def fn(n):
    count = 0
    for i in range(1,n+1):
        for j in range(1,n+1):
            if(i*i*i == j*j):
                if(i<=j):
                    if(i<n and j<n):
                       count+=1
    return count

n = int(input())
count = fn(n)
print(count)