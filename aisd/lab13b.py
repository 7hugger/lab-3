#DFS
import tkinter as tk
import random

# ====== settings ======
N=10; CELL=40; LINE=4; BRAID=0.15
BG='#0f1115'; WALLC='#23262d'; FREEC='#f0f3f6'; GRID='#404350'
START='#6a5acd'; EXIT='#2e8b57'; PATH='#39d353'; ROACH='#e53935'
DIRS=['N','E','S','W']; OFF={'N':(-1,0),'E':(0,1),'S':(1,0),'W':(0,-1)}; OPP={'N':'S','S':'N','E':'W','W':'E'}
ORIENT_BASE='up'  

# ====== side-walls maze ======
class Maze:
    def __init__(self,n):
        self.n=n
        self.w=[[set(DIRS) for _ in range(n)] for _ in range(n)]

    def inside(self,r,c):
        return 0<=r<self.n and 0<=c<self.n

    def neigh(self,r,c):
        for d,(dr,dc) in OFF.items():
            rr,cc=r+dr,c+dc
            if self.inside(rr,cc):
                yield d,rr,cc

    def knock(self,r,c,d):
        self.w[r][c].discard(d)
        dr,dc=OFF[d]; rr,cc=r+dr,c+dc
        if self.inside(rr,cc):
            self.w[rr][cc].discard(OPP[d])

    def prim(self,rng):
        n=self.n; vis=[[False]*n for _ in range(n)]; sr=sc=0; vis[sr][sc]=1
        F=[(sr,sc,d) for d,_,_ in self.neigh(sr,sc)]
        while F:
            i=rng.randrange(len(F)); r,c,d=F.pop(i); dr,dc=OFF[d]; rr,cc=r+dr,c+dc
            if not vis[rr][cc]:
                self.knock(r,c,d); vis[rr][cc]=1
                for d2,rr2,cc2 in self.neigh(rr,cc):
                    if not vis[rr2][cc2]:
                        F.append((rr,cc,d2))

    def braid(self,rng,p):
        cells=[(r,c) for r in range(self.n) for c in range(self.n) if 4-len(self.w[r][c])==1]
        rng.shuffle(cells)
        for r,c in cells:
            if rng.random()<p:
                cand=[d for d,_,_ in self.neigh(r,c) if d in self.w[r][c]]
                if cand:
                    self.knock(r,c,rng.choice(cand))

    def bitmap(self):
        n=self.n; H=2*n+1; B=[[1]*H for _ in range(H)]
        for r in range(n):
            for c in range(n):
                br,bc=2*r+1,2*c+1; B[br][bc]=0
                if 'N' not in self.w[r][c]: B[br-1][bc]=0
                if 'S' not in self.w[r][c]: B[br+1][bc]=0
                if 'W' not in self.w[r][c]: B[br][bc-1]=0
                if 'E' not in self.w[r][c]: B[br][bc+1]=0
        return B

# ====== app ======
class App:
    def __init__(self, root):
        self.rng=random.Random()
        self.m=Maze(N)
        self.start=(0,1); self.goal=(N-1,N-1)
        self.path=[]
        self.stack=[]; self.seen=set(); self.parents={}
        self.searching=False; self.running=False
        self.roach=None; self.last_dir='S'

        W=N*CELL+LINE; H=N*CELL+LINE
        self.cv=tk.Canvas(root,width=W,height=H,bg=BG,highlightthickness=0)
        self.cv.grid(row=0,column=0,columnspan=4,padx=12,pady=12)

        tk.Button(root,text='Сгенерировать',command=self.gen).grid(row=1,column=0,padx=6,pady=(0,12),sticky='ew')
        self.run_btn=tk.Button(root,text='Пустить робота (DFS)',command=self.start_search)
        self.run_btn.grid(row=1,column=1,columnspan=3,padx=6,pady=(0,12),sticky='ew')
                
        self.st=tk.StringVar(value='Готово.')
        tk.Label(root,textvariable=self.st,anchor='w',fg='#e7e7e7',bg=BG).grid(row=2,column=0,columnspan=4,sticky='ew',padx=12,pady=(0,12))

        self.gen()

    def gen(self):
        s = g = 1  # Инициализация для статуса
        for _ in range(100):
            self.m=Maze(N); self.m.prim(self.rng); self.m.braid(self.rng,BRAID)
            odd=[c for c in range(N) if c%2==1]
            s=self.rng.choice(odd); g=self.rng.choice(odd)
            self.start=(0,s); self.goal=(N-1,g)
            self.m.w[0][s].discard('N'); self.m.w[N-1][g].discard('S')
            if self._has_path(self.start,self.goal):
                break
        self.path=[]; self.stack=[]; self.seen=set(); self.parents={}; self.searching=False; self.running=False
        self.run_btn.config(state='normal')
        self.draw(); self.st.set(f'Prim+Braid лабиринт {N}×{N}. Вход ↑{s}, выход ↓{g}.')

    def _has_path(self, start, goal):
        # Простая итеративная проверка на путь с DFS (без анимации)
        stack = [start]; seen = {start}; parents = {start: None}
        while stack:
            r,c = stack.pop()
            if (r,c) == goal:
                return True
            for d,rr,cc in self.m.neigh(r,c):
                neigh_cell = (rr,cc)
                if d not in self.m.w[r][c] and neigh_cell not in seen:
                    seen.add(neigh_cell); parents[neigh_cell] = (r,c); stack.append(neigh_cell)
        return False

    def start_search(self):
        if self.searching: return
        self.stack=[self.start]; self.seen={self.start}; self.parents={self.start:None}
        self.searching=True; self.running=True
        self.run_btn.config(state='disabled')
        self.draw(); self.st.set('Поиск запущен (DFS)…')
        self._tick()

    def search_step(self):
        if not self.searching or not self.stack:
            self.st.set('Поиск остановлен.'); return False
        r,c=self.stack[-1]
        if (r,c)==self.goal:
            path=[]; cur=(r,c)
            while cur is not None:
                path.append(cur); cur=self.parents.get(cur)
            self.path=path[::-1]
            self.searching=False
            self.draw(); self.st.set('Таракан нашёл выход!')
            return False
        neigh=[(d,rr,cc) for d,rr,cc in self.m.neigh(r,c) if d not in self.m.w[r][c] and (rr,cc) not in self.seen]
        random.shuffle(neigh)
        if neigh:
            d,rr,cc=neigh[0]
            prev=(r,c); cur=(rr,cc)
            self.stack.append(cur); self.seen.add(cur); self.parents[cur]=prev
            self.draw_roach(cur, self.dir_from(prev,cur))
            return True
        self.stack.pop()
        if not self.stack:
            self.st.set('Тупик. Выход не найден.'); self.searching=False; return False
        cur=self.stack[-1]
        self.draw_roach(cur, self.dir_from((r,c),cur))
        return True

    def draw(self):
        self.cv.delete('all')
        for r in range(N):
            for c in range(N):
                x0,y0=c*CELL,r*CELL; x1,y1=x0+CELL,y0+CELL
                self.cv.create_rectangle(x0,y0,x1,y1,fill=FREEC,outline=GRID)
        for r in range(N):
            for c in range(N):
                x0,y0=c*CELL,r*CELL; x1,y1=x0+CELL,y0+CELL
                if 'N' in self.m.w[r][c]: self.cv.create_line(x0,y0,x1,y0,fill=WALLC,width=LINE)
                if 'W' in self.m.w[r][c]: self.cv.create_line(x0,y0,x0,y1,fill=WALLC,width=LINE)
                if r==N-1 and 'S' in self.m.w[r][c]: self.cv.create_line(x0,y1,x1,y1,fill=WALLC,width=LINE)
                if c==N-1 and 'E' in self.m.w[r][c]: self.cv.create_line(x1,y0,x1,y1,fill=WALLC,width=LINE)
        self.hi(self.start,START); self.hi(self.goal,EXIT)
        for (r,c) in self.path:
            cx=c*CELL+CELL//2; cy=r*CELL+CELL//2; rad=max(3, CELL//8)
            self.cv.create_oval(cx-rad, cy-rad, cx+rad, cy+rad, fill=PATH, outline='')
        pos = self.stack[-1] if (self.searching and self.stack) else (self.path[-1] if self.path else self.start)
        self.draw_roach(pos, self.last_dir)

    def hi(self,cell,color,alpha=1.0):
        r,c=cell; x0,y0=c*CELL+4,r*CELL+4; x1,y1=x0+CELL-8,y0+CELL-8
        if alpha>=1.0:
            self.cv.create_rectangle(x0,y0,x1,y1,fill=color,outline='')
        else:
            h=int((CELL-8)*alpha)
            for i in range(h):
                self.cv.create_line(x0,y0+i,x1,y0+i,fill=color)

    def draw_roach(self,cell,direction=None):
        r,c=cell; cx=c*CELL+CELL//2; cy=r*CELL+CELL//2
        if direction: self.last_dir=direction
        if self.roach: self.cv.delete(self.roach)
        rad=CELL//3
        self.roach=self.cv.create_oval(cx-rad,cy-rad,cx+rad,cy+rad,fill=ROACH,outline='#550000')

    def dir_from(self,a,b):
        ra,ca=a; rb,cb=b
        if rb==ra-1: return 'N'
        if rb==ra+1: return 'S'
        if cb==ca+1: return 'E'
        return 'W'

    def _tick(self):
        if not self.running: return
        cont=self.search_step()
        if cont: self.cv.after(100,self._tick)
        else:
            self.running=False
            self.run_btn.config(state='normal')

    def save_cells(self):
        return

    def save_walls(self):
        return


def main():
    root=tk.Tk(); root.title('Робот — лабиринт 10×10 (DFS)'); root.configure(bg=BG)
    App(root)
    root.mainloop()

if __name__=='__main__':
    main()
