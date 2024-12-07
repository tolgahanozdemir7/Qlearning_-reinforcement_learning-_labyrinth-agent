import numpy as np

labirent = np.array([[-100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100],
                    [-100,   -1,   -1, -100,   -1,   -1,   -1,   -1,   -1,   -1,   -1, -100,   -1, -100, -100],
                    [-100,   -1, -100, -100,   -1, -100, -100, -100,   -1, -100,   -1, -100,   -1,   -1, -100],
                    [-100,   -1, -100,   -1, -100,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1, -100],
                    [-100, -100,   -1,   -1, -100,   -1, -100, -100, -100,   -1,   -1,   -1,   -1,   -1, -100],
                    [-100,   -1,   -1, -100,   -1,   -1, -100,   -1, -100, -100,   -1, -100,   -1,   -1, -100],
                    [-100, -100, -100, -100,   -1, -100, -100,   -1,   -1,   -1,   -1,   -1, -100,   -1, -100],
                    [-100, -100,   -1,   -1,   -1,   -1,   -1,   -1, -100,   -1,   -1,   -1, -100,   -1, -100],
                    [-100,   -1, -100,   -1, -100,   -1, -100,   -1,   -1,   -1, -100, -100,   -1,   -1, -100],
                    [-100,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1, -100],
                    [-100, -100,   -1, -100,   -1, -100, -100,   -1, -100, -100, -100,   -1,   -1, -100, -100],
                    [-100,   -1,   -1, -100,   -1, -100,   -1,   -1,   -1, -100,   -1,   -1, -100,   -1, -100],
                    [-100, -100,   -1, -100,   -1, -100,   -1, -100, -100,   -1, -100,   -1, -100,   -1, -100],
                    [-100,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1, -100,   -1, -100]
                    ])

print("Labirent\n",labirent)

labirent_satir_sayisi,labirent_sutun_sayisi=labirent.shape
q_degerleri=np.zeros((labirent_satir_sayisi,labirent_sutun_sayisi,4))
hareketler=["SAG","SOL","YUKARI","ASAGI"]
#%%
def engel_mi(gecerli_satir_index,gecerli_sutun_index):
    if labirent[gecerli_satir_index,gecerli_sutun_index]==1:
        return False
    else:
        return True
#%%       
def baslangic_belirle():
    gecerli_satir_index=np.random.randint(labirent_satir_sayisi)
    gecerli_sutun_index=np.random.randint(labirent_sutun_sayisi)
    while engel_mi(gecerli_satir_index,gecerli_sutun_index):
         gecerli_satir_index=np.random.randint(labirent_satir_sayisi)   
         gecerli_sutun_index=np.random.randint(labirent_sutun_sayisi)
    return gecerli_satir_index,gecerli_sutun_index     
#%%
def hareket_belirle(gecerli_satir_index,gecerli_sutun_index,epsilon):
    if np.random.random()<epsilon:
        return np.argmax(q_degerleri[gecerli_satir_index,gecerli_sutun_index])
    else:
        return np.random.randint(4)
#%%

def hareket_et(gecerli_satir_index,gecerli_sutun_index,hareket_index):
    yeni_satir_index=gecerli_satir_index
    yeni_sutun_index=gecerli_sutun_index
    
    if hareketler[hareket_index]=="SAG" and gecerli_sutun_index<labirent_sutun_sayisi-1:
        yeni_sutun_index+=1
    elif hareketler[hareket_index]=="SOL" and gecerli_sutun_index>0:
        yeni_sutun_index-=1
    elif hareketler[hareket_index]=="YUKARI" and gecerli_satir_index>0:
        yeni_satir_index-=1
    elif hareketler[hareket_index]=="ASAGI" and gecerli_satir_index<labirent_satir_sayisi-1:
        yeni_sutun_index+=1  
    return yeni_satir_index,yeni_sutun_index
#%%        
def en_kisa_yol(bas_satir_index,baslangic_sutun_index):
    if engel_mi(bas_satir_index,baslangic_sutun_index):
        return []
    else:
        gecerli_satir_index,gecerli_sutun_index=bas_satir_index,baslangic_sutun_index
        en_kisa=[]
        en_kisa.append([gecerli_satir_index,gecerli_sutun_index])
        while not engel_mi(gecerli_satir_index,gecerli_sutun_index):
           hareket_index=hareket_belirle(gecerli_satir_index,gecerli_sutun_index,1)
           gecerli_satir_index,gecerli_sutun_index=hareket_et(gecerli_satir_index,gecerli_sutun_index,hareket_index)
           en_kisa.append([gecerli_satir_index,gecerli_sutun_index])
        return en_kisa
#%%
epsilon=0.9
azalma_degeri=0.9
ogrenme_orani=0.9
#%%
for adim in range(1000):
    satir_index,sutun_index=baslangic_belirle()
    while not engel_mi(satir_index,sutun_index):
        hareket_index=hareket_belirle(satir_index,sutun_index,epsilon)
        eski_satir_index,eski_sutun_index=satir_index,sutun_index
        satir_index,sutun_index=hareket_et(satir_index,sutun_index, hareket_index)
        odul=labirent[satir_index,sutun_index]
        eski_q_degeri=q_degerleri[eski_satir_index,eski_sutun_index,hareket_index]
        fark=odul+(azalma_degeri*np.max(q_degerleri[satir_index,sutun_index]))-eski_q_degeri
        yeni_q_degeri=eski_q_degeri + (ogrenme_orani*fark)
        q_degerleri[eski_satir_index,eski_sutun_index,hareket_index]=yeni_q_degeri
print("egitim tamamlandi")        
#%%     

baslangic_satir,baslangic_sutun=input("robotun baslangic konumunu girin \n").split()
baslangic_satir=int(baslangic_satir)
baslangic_sutun=int(baslangic_sutun)
en_kisa_rota=en_kisa_yol(int(baslangic_satir),int(baslangic_sutun))
if not en_kisa_rota:
    print("konum gecersiz")
else:
    print("cikisa giden rota")
    for i in range(len(en_kisa_rota)):
        print(en_kisa_rota[i])
#%%
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output
import time

def ciz_labirent_ve_ajan_ve_yol(labirent,ajan_konumu,baslangic_konumu,yol):
    fig,ax=plt.subplots()
    ax.imshow(labirent,cmap='gray')
    
    for i in range(labirent.shape[0]):
        for j in range(labirent.shape[1]):
            if labirent[i,j]==-1:
                renk='green' if (i,j) == baslangic_konumu else 'red'
                circle =plt.Circle((j,i),0.3,color=renk)
                ax.add_patch(circle)
            elif labirent[i,j] == -100:
                ax.text(j,i,'X',ha='center',va='center',color='red',fontsize=8)
            elif labirent[i,j]==100:
                ax.text(j,i,'Hedef',ha='center',va='center',color='green',fontsize=8)
                
    yol_np=np.array(yol)
    ax.plot(yol_np[:,1],yol_np[:,0],color='blue',linewidth=1)
    
    ax.plot(ajan_konumu[1],ajan_konumu[0],'ba',markersize=15)
    
    ax.tick_params(axis='x',labelsize=8)
    ax.tick_params(axis='y',labelsize=8)
    
    ax.set_aspect('equal',adjustable='box')
    plt.subplots_adjust(left=0,right=1,top=1,bottom=0)
    plt.show()
    
ciz_labirent_ve_ajan_ve_yol(labirent,en_kisa_rota[0],(baslangic_satir,baslangic_sutun),en_kisa_rota)
    
for konum in en_kisa_rota[1:]:
    clear_output(wait=True)
    ciz_labirent_ve_ajan_ve_yol(labirent, konum,(baslangic_satir,baslangic_sutun),en_kisa_rota)    
    time.sleep(0.05)            






   
            






