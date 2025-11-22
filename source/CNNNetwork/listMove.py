def list_move():
    list=[]
    def in_bound(x,y):
        if x>7 or x<0 or y>7 or y<0:
            return 0
        return 1
    file=['a','b','c','d','e','f','g','h']
    rank=['8','7','6','5','4','3','2','1']
    for f in range(8):
        for r in range(8):
            for i in range(1,8,1):
                if in_bound(f+i,r):list.append(file[f]+rank[r]+file[f+i]+rank[r])
                if in_bound(f-i,r):list.append(file[f]+rank[r]+file[f-i]+rank[r])
                if in_bound(f,r+i):list.append(file[f]+rank[r]+file[f]+rank[r+i])
                if in_bound(f,r-i):list.append(file[f]+rank[r]+file[f]+rank[r-i])
                if in_bound(f+i,r+i):list.append(file[f]+rank[r]+file[f+i]+rank[r+i])
                if in_bound(f-i,r-i):list.append(file[f]+rank[r]+file[f-i]+rank[r-i])
                if in_bound(f-i,r+i):list.append(file[f]+rank[r]+file[f-i]+rank[r+i])
                if in_bound(f+i,r-i):list.append(file[f]+rank[r]+file[f+i]+rank[r-i])
            if in_bound(f+1,r+2):list.append(file[f]+rank[r]+file[f+1]+rank[r+2])
            if in_bound(f+1,r-2):list.append(file[f]+rank[r]+file[f+1]+rank[r-2])
            if in_bound(f-1,r+2):list.append(file[f]+rank[r]+file[f-1]+rank[r+2])
            if in_bound(f-1,r-2):list.append(file[f]+rank[r]+file[f-1]+rank[r-2])
            if in_bound(f+2,r+1):list.append(file[f]+rank[r]+file[f+2]+rank[r+1])
            if in_bound(f+2,r-1):list.append(file[f]+rank[r]+file[f+2]+rank[r-1])
            if in_bound(f-2,r+1):list.append(file[f]+rank[r]+file[f-2]+rank[r+1])
            if in_bound(f-2,r-1):list.append(file[f]+rank[r]+file[f-2]+rank[r-1])
            if r==1:
                if in_bound(f,r-1):list.append(file[f]+rank[r]+file[f]+rank[r-1]+'q')
                if in_bound(f,r-1):list.append(file[f]+rank[r]+file[f]+rank[r-1]+'r')
                if in_bound(f,r-1):list.append(file[f]+rank[r]+file[f]+rank[r-1]+'b')
                if in_bound(f,r-1):list.append(file[f]+rank[r]+file[f]+rank[r-1]+'n')
                if in_bound(f+1,r-1):list.append(file[f]+rank[r]+file[f+1]+rank[r-1]+'q')
                if in_bound(f+1,r-1):list.append(file[f]+rank[r]+file[f+1]+rank[r-1]+'r')
                if in_bound(f+1,r-1):list.append(file[f]+rank[r]+file[f+1]+rank[r-1]+'b')
                if in_bound(f+1,r-1):list.append(file[f]+rank[r]+file[f+1]+rank[r-1]+'n')
                if in_bound(f-1,r-1):list.append(file[f]+rank[r]+file[f-1]+rank[r-1]+'q')
                if in_bound(f-1,r-1):list.append(file[f]+rank[r]+file[f-1]+rank[r-1]+'r')
                if in_bound(f-1,r-1):list.append(file[f]+rank[r]+file[f-1]+rank[r-1]+'b')
                if in_bound(f-1,r-1):list.append(file[f]+rank[r]+file[f-1]+rank[r-1]+'n')
            if r==6:
                if in_bound(f,r+1):list.append(file[f]+rank[r]+file[f]+rank[r+1]+'q')
                if in_bound(f,r+1):list.append(file[f]+rank[r]+file[f]+rank[r+1]+'r')
                if in_bound(f,r+1):list.append(file[f]+rank[r]+file[f]+rank[r+1]+'b')
                if in_bound(f,r+1):list.append(file[f]+rank[r]+file[f]+rank[r+1]+'n')
                if in_bound(f+1,r+1):list.append(file[f]+rank[r]+file[f+1]+rank[r+1]+'q')
                if in_bound(f+1,r+1):list.append(file[f]+rank[r]+file[f+1]+rank[r+1]+'r')
                if in_bound(f+1,r+1):list.append(file[f]+rank[r]+file[f+1]+rank[r+1]+'b')
                if in_bound(f+1,r+1):list.append(file[f]+rank[r]+file[f+1]+rank[r+1]+'n')
                if in_bound(f-1,r+1):list.append(file[f]+rank[r]+file[f-1]+rank[r+1]+'q')
                if in_bound(f-1,r+1):list.append(file[f]+rank[r]+file[f-1]+rank[r+1]+'r')
                if in_bound(f-1,r+1):list.append(file[f]+rank[r]+file[f-1]+rank[r+1]+'b')
                if in_bound(f-1,r+1):list.append(file[f]+rank[r]+file[f-1]+rank[r+1]+'n')
    return list