def tr(n):
    s=''
    while n!=0:
        s=str(n%6)+s
        n=n//6
    return s

a=[]
for n in range(100,1000):
    x=str(int(n))
    if int(x)%100==0:
        continue
    b=''
    s1=int((x[0])+(x[1]))
    s2=int((x[1])+(x[2]))
    s3=int((x[2])+(x[0]))
    lst=[s1,s2,s3]
    nlst=lst
    for i in range(len(lst)):
        if len(str(lst[i]))==1:
            lst.pop(i)
            break
    b=abs(max(lst)-min(lst))
    if b=='5':
        a.append(n)
print(min(a))