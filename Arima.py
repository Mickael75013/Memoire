import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2


def Prediction(file,file2):


    f = open(file, "r")
    f2 = open(file2,"w")

    # Création des listes de valeurs

    # Liste des valeurs de SP02 extraites à partir du fichier contenant le jeu de données
    SP02_values = []

    # Liste de valeurs de Heart rate extraites
    HR_values = []

    # Liste de valeurs de Blood Pressure
    BP_values = []

    # Lecture du fichier et stockage de chacune des lignes du jeu de données dans le tableau lines
    # Chaque valeur du tableau lines correpond à une ligne du fichier
    lines = f.readlines()

    # La somme des résidus
    Sum_error_rate=0

    # Affichage des deux premières lignes du dataset contenant les noms des paramètres de santé ainsi que leurs unités
    print(lines[0])
    print(lines[1])

    line0=lines[0]
    line1=lines[1]

    f2.write(line0)
    f2.write((line1))
    f2.write("\n");f2.write("\n")

    lines.remove(lines[0])
    lines.remove(lines[0])

    for l in lines:

        newLine1 = l.replace("\n", "")
        newLine2 = newLine1.split(',')

        # Conversion des valeurs de str à float
        newLine2[2]=float(newLine2[2])
        newLine2[4]=float(newLine2[4])
        newLine2[7]=float(newLine2[7])

        # Ajout des valeurs de chaque paramètre à une liste
        HR_values.append(newLine2[4])
        BP_values.append((newLine2[2]))
        SP02_values.append((newLine2[7]))

    print("Liste des valeurs de SP02 : ")
    print(SP02_values)
    print(SP02_values.__len__())
    print(type(SP02_values[0]))

    print("Liste des valeurs de Heart Rate : ")
    print(HR_values)
    print(HR_values.__len__())
    print(type(HR_values[0]))

    print("Liste des valeurs de Blood Pressure : ")
    print(BP_values)
    print(BP_values.__len__())
    print(type(BP_values[0]))

    f2.write("Liste des valeurs de SP02 : ")
    f2.write("\n");f2.write("\n")
    list=str(SP02_values)
    f2.write(list)
    f2.write("\n");f2.write("\n");f2.write("\n")
    f2.write("Liste des valeurs de Heart Rate : ")
    f2.write("\n");f2.write("\n")
    list=str(HR_values)
    f2.write(list)
    f2.write("\n")
    f2.write("\n");f2.write("\n");f2.write("\n")
    f2.write("Liste des valeurs de Blood Pressure : ")
    f2.write("\n");f2.write("\n")
    list=str(SP02_values)
    f2.write(list)
    f2.write('\n')
    f2.write("\n")

    # taille de la fenetre des sous-listes de valeurs utilisées pour la prédiction
    n=12

    # Indice dans la liste des valeurs de Heart Rate
    i=0


    HR_list=[]
    HR_subset=[]
    SP02_list=[]
    SP02_subset=[]



    for valeur in HR_values:
        if i<n:

            if(i!=0):
                if(HR_values[i]+10<HR_values[i-1] or HR_values[i]-10>HR_values[i-1]):
                    HR_subset.append(HR_values[i])


                    i=i+1


                else:
                    HR_subset.append(HR_values[i])
                    i = i + 1
            else:
                HR_subset.append(HR_values[0])
                i=i+1


        else:

            HR_list.append(HR_subset)
            n=n+12

            HR_subset=[]
            if (HR_values[i]+10 < HR_values[i-1] or HR_values[i]-10 > HR_values[i-1]):
                HR_subset.append(HR_values[i])
                i = i + 1
            else:
                HR_subset.append(HR_values[i])
                i = i + 1

    i = 0
    n = 12

    for valeur in SP02_values:
        if i<n:

            if(i!=0):
                if(SP02_values[i]+10<SP02_values[i-1] or SP02_values[i]-10>SP02_values[i-1]):
                    HR_subset.append(HR_values[i])


                    i=i+1


                else:
                    SP02_subset.append(SP02_values[i])
                    i = i + 1
            else:
                SP02_subset.append(SP02_values[0])
                i=i+1


        else:

            SP02_list.append(SP02_subset)
            n=n+12

            SP02_subset=[]
            if (SP02_values[i]+10 < SP02_values[i-1] or SP02_values[i]-10 > SP02_values[i-1]):
                SP02_subset.append(SP02_values[i])
                i = i + 1
            else:
                SP02_subset.append(SP02_values[i])
                i = i + 1


    List_len=[]
    for val in SP02_list:
        x= len(val)
        List_len.append(x)

    print(List_len)




    BP_list = []
    BP_subset = []
    i=0
    n=12

    for valeur in BP_values:
        if i<n:

            if(i!=0):
                if(BP_values[i]+10<BP_values[i-1] or BP_values[i]-10>BP_values[i-1]):
                    BP_subset.append(BP_values[i])
                    i=i+1


                else:
                    BP_subset.append(BP_values[i])
                    i = i + 1
            else:
                BP_subset.append(BP_values[0])
                i=i+1


        else:

            # On ajoute la sous liste de 12 valeurs de BP à la liste contenant toutes les sous listes de BP
            BP_list.append(BP_subset)

            n=n+12

            BP_subset=[]
            if (BP_values[i]+10 < BP_values[i-1] or BP_values[i]-10 > BP_values[i-1]):
                BP_subset.append(BP_values[i])
                i = i + 1
            else:
                BP_subset.append(BP_values[i])
                i = i + 1

    print(BP_list)

    List_len = []
    for val in BP_list:
        x = len(val)
        List_len.append(x)

    print(List_len)








    print("Prédiction avec des séries temporelles de valeurs de paramètres physiologiques")
    print("\n")

    print("Liste des valeurs de Heart rate :")
    print(HR_values)
    print("\n")

    # Liste contenant des sous listes de valeurs de prédictions
    Forecast_list=[]


    # Listes contenant toutes les valeurs de prédictions
    Forecast_values=[]


    # Listes contenant toutes les résidus temporelles
    Error_rate_list=[]



    # Arima
    # Prédictions d'une sous liste de valeur d'un paramètre de santé avec Arima


    print(SP02_list)


    def Arima(param):

        index = 0
        List_values=[]
        if(param=="HR_list"):
            List_values=HR_list
        if(param=="BP_list"):
            List_values=BP_list
        if(param=="SP02_list"):
            List_values=SP02_list

        print(List_values)
        Sum_error_rate=0

        # Pour chaque sous-liste de la liste composé de sous listes de valeurs d'un paramètre de santé
        for l in List_values:

            print("Sous-liste des valeurs de", param, " : ")
            print(l)
            print("\n")
            print("Moyenne des valeurs de cette sous-liste : ")
            print(moyenne(l))
            print("\n")
            print("Prédiction de la moyenne pour la prochaine liste de valeurs : ")
            print("On peut prédire que la moyenne des valeurs de la prochaine liste sera comprise dans un intervalle entre : [",moyenne(l) - 10, " , ", moyenne(l) + 10, "]")

            model = sm.tsa.ARIMA(l, order=(2, 1, 1))

            # Ajuster le modèle aux données
            result = model.fit()

            # Prédire les 12 prochaines valeurs
            forecast = result.forecast(steps=12)

            for x in forecast:
                Forecast_values.append(x)

            forecast1=[]
            for x in forecast:
                forecast1.append(x)

            print("Voici la prédiction des valeurs de la prochaine sous-liste : ")
            print(forecast1)
            print('\n')
            print("**************************************************************************************************************************************************************************")

            Forecast_list.append(forecast1)


            #Indice dans la liste forecast
            i = 0

            # Index sert à ne pas prendre en compte la première sous-liste de valeurs réelles car il n'y a pas de valeurs de prédictions à comparer avec la 1ère sous liste puisque ces prédictions ont été émises à partir de la 1ère sous-liste
            Error_rate=0
            if (index != 0 and index!=List_values.__len__()-1):

                Next_index_real_list_values = index+1

                for val in List_values[Next_index_real_list_values]:
                    if(val==forecast1[i]):
                        i+=1
                        Error_rate_list.append(Error_rate)
                    else:
                        Error_rate_list.append(abs(forecast1[i] - val))
                        Sum_error_rate+=abs(forecast1[i]-val)
                        i+=1
            else:
                #On vérifie qu'on va pas comparer la dernière liste de HR_list avec une liste q
                if(index!=List_values.__len__()-1):
                    # On va comparer chaque valeur prédite avec chaque valeur réelles de la prochaine liste de HR
                    for val in List_values[1]:
                        if(forecast1[i]==val):
                            i=i+1
                            Error_rate_list.append(Error_rate)
                        else:
                            Error_rate_list.append(abs(forecast1[i]-val))
                            Sum_error_rate+=abs(forecast1[i]-val)
                            i=i+1
                index=index+1
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(len(Forecast_values))
        return(Forecast_list, Error_rate_list, Sum_error_rate, Forecast_values)



    # A partir de la 1ère sous-liste de valeurs réelles d'une taille de 12 d'un paramètre de santé on va prédire les 12 prochaines valeurs et on va comparer ces valeurs prédites avec les valeurs réelles.
    # Pour la n-ième valeur prédite on va la comparer avec la n-ième valeur réelle de la sous liste de valeurs réelles d'un seul paramètre de santé
    # On va effectuer le calcul :
    #  Pour tous les valeurs prédites d'une liste de taille 12 avec toutes les valeurs réelles d'une sous liste on va calculer les résidus et effectuer un calcul de la moyenne des résidus
    #  Résidus n = valeur absolue( valeur réelle - valeur prédite)
    #

    # Fonction pour calculer la précsion du modèle Arima appliquée sur un paramètre de santé donnée en argument de la fonction

    def precision(param):
        if(param=="SP02"):
            Arima_results=Arima("SP02_list")
            list=SP02_list
        if(param=="HR"):
            Arima_results = Arima("HR_list")
            list=HR_list
        if (param=="BP"):
            Arima_results = Arima("BP_list")
            list=BP_list



        Forecast_list=Arima_results[0]
        Error_rate_list=Arima_results[1]
        Sum_error_rate=Arima_results[2]
        Forecast_values=Arima_results[3]



        #On va retirer la dernière liste de prédiction car elle n'est comparable avec aucune liste de valeurs réelles


        Forecast_list.remove(Forecast_list[len(Forecast_list)-1])
        print("Longeur de la liste contenant des sous-listes de valeurs réelles de ",param,":",len(list))
        print("Longeur de la liste contenant des sous-listes de prédictions de valeur", param," :",len(Forecast_list))
        print("\n")
        Precision= 100-(Sum_error_rate / (SP02_values.__len__() - 12))
        print(("Précision du modèle Arima : "),(Precision))
        return(Forecast_values)







    # Fonction pour créer des figures décrivant une comparaison des deux courbes des valeurs réelles d'un paramètre de santé avec les valeurs prédites en fonction du temps
    def figure(param,num_fig):

        # On a utilise les 12 premières valeurs d'un paramètre de santé pour prédire les 12 prochaines valeurs de ce meme paramètre.
        # On pourra alors comparer les 12 valeurs prédites avec les 12 prochaines valeurs et voir si les prédiction sont précisies.
        # Donc la 1ère sous liste des valeurs n'est comparable avec aucune liste de valeurs prédites.
        # Pour réaliser une figure de comparaison des valeurs prédites avec les valeurs mesurées, on va supprimer les 12 premières valeurs de la liste de valeurs réelles car on ne peut pas la comparer avec une liste de valeurs prédites.

        if(param=="SP02"):
            list_values=SP02_values
        if(param=="Blood Pressure"):
            list_values=BP_values
        if(param=="Heart Rate"):
            list_values=HR_values


        i=0
        while(i<12):
            list_values.remove(list_values[0])
            i+=1

        y=list_values
        l= len(list_values)
        Time=[]
        i=0
        while(i<l):
            Time.append(i)
            i=i+1


        print(list_values)

        print(len(list_values))


        print(Forecast_values)
        print("len forcast values",len(Forecast_values))

        x = Time
        title="Comparison of predicted "+param+" value with "+param+" reals values"
        plt.title(title)
        plt.plot(x,y)
        plt.plot(x,Forecast_values)
        plt.xlabel("Time (seconds)")
        ylabel= param+" values"
        plt.ylabel(ylabel)

        ylabel2=param+" values (bleu curve)   and " +param+"   Forecast values (orange curve) "
        plt.ylabel(ylabel2)
        file_path = "C:\\Users\micka\OneDrive\Bureau\Stage\\"
        Fig_name="Fig"+str(num_fig)+".jpg"
        plt.savefig(file_path + Fig_name)
        plt.show()

    Forecast_values = precision("BP")
    figure("Blood Pressure", 3)



    Forecast_list=[]
    Forecast_values=[]

    Forecast_values = precision("SP02")
    figure("SP02", 2)

    Forecast_list=[]
    Forecast_values=[]
    Forecast_values=precision("HR")
    figure("Heart Rate",1)

def moyenne(liste):
    somme=0
    for valeur in liste:
        somme+=valeur
    moyenne= somme / len(liste)
    return(moyenne)




file="C:\\Users\micka\OneDrive\Bureau\Arima\TrainDataset.csv"
file2="C:\\Users\micka\OneDrive\Bureau\Stage\\results.txt"

Prediction(file, file2)
