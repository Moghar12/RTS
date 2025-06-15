Vous voulez dire l'algorithme en pseudo-code ou sous forme de code exécutable ?
Si vous cherchez un pseudo-code qui résume la logique de l'ordonnanceur basée sur le code C fourni, voici :
Algorithme d'Ordonnancement à Priorité Fixe (Pseudo-code)
Début Algorithme

    // 1. Initialisation
    Demander le NOMBRE_DE_TACHES (n)
    Pour chaque TACHE i de 1 à n :
        Demander les paramètres (TEMPS_ARRIVEE, TEMPS_EXECUTION, ECHEANCE, PERIODE)
        SI i est la première tâche : TACHE_i.PRIORITE = 1
        SINON SI i est la deuxième tâche : TACHE_i.PRIORITE = 2
        SINON SI i est la troisième tâche : TACHE_i.PRIORITE = 3
        SINON : TACHE_i.PRIORITE = 99 (priorité par défaut)
        Initialiser TACHE_i.TEMPS_EXECUTION_RESTANT = TACHE_i.TEMPS_EXECUTION
        Initialiser TACHE_i.INSTANCE = 0
        Initialiser TACHE_i.PRET = FAUX
        Calculer TACHE_i.TEMPS_ARRIVEE_ABSOLU = TACHE_i.TEMPS_ARRIVEE + (TACHE_i.INSTANCE * TACHE_i.PERIODE)
        Calculer TACHE_i.ECHEANCE_ABSOLUE = TACHE_i.TEMPS_ARRIVEE_ABSOLU + TACHE_i.ECHEANCE

    Calculer UTILISATION_CPU = Somme (TACHE_i.TEMPS_EXECUTION / TACHE_i.PERIODE) pour toutes les tâches
    Calculer HYPERPERIODE = PPCM (PERIODE de toutes les tâches)

    // 2. Boucle de Simulation
    INITIALISER TEMPS_COURANT = 0
    INITIALISER TACHE_ACTIVE_ID = AUCUNE_TACHE

    TANT QUE TEMPS_COURANT <= HYPERPERIODE :

        // 2.1. Déclenchement des Tâches (point d'ordonnancement)
        Pour chaque TACHE i de 1 à n :
            SI TACHE_i.TEMPS_ARRIVEE_ABSOLU == TEMPS_COURANT :
                TACHE_i.PRET = VRAI
                // Si de nouvelles tâches arrivent, ou si l'ancienne tâche est terminée,
                // ou si aucune tâche n'était active, re-sélectionner la tâche active.
                // Cela est géré par la logique suivante.

        // 2.2. Sélection de la Tâche à Exécuter
        TACHE_AYANT_PLUS_HAUTE_PRIORITE = AUCUNE_TACHE
        PLUS_HAUTE_PRIORITE_TROUVEE = INFINI

        Pour chaque TACHE i de 1 à n :
            SI TACHE_i.PRET est VRAI ET TACHE_i.TEMPS_EXECUTION_RESTANT > 0 :
                SI TACHE_i.PRIORITE < PLUS_HAUTE_PRIORITE_TROUVEE :
                    PLUS_HAUTE_PRIORITE_TROUVEE = TACHE_i.PRIORITE
                    TACHE_AYANT_PLUS_HAUTE_PRIORITE = TACHE_i.ID

        TACHE_ACTIVE_ID = TACHE_AYANT_PLUS_HAUTE_PRIORITE

        // 2.3. Exécution
        SI TACHE_ACTIVE_ID est AUCUNE_TACHE :
            Afficher "TEMPS_COURANT : Inactif"
        SINON :
            Décrémenter TACHE_ACTIVE_ID.TEMPS_EXECUTION_RESTANT de 1
            Afficher "TEMPS_COURANT : Tâche TACHE_ACTIVE_ID en exécution"

            // 2.4. Fin d'une Instance de Tâche
            SI TACHE_ACTIVE_ID.TEMPS_EXECUTION_RESTANT == 0 :
                Afficher "Tâche TACHE_ACTIVE_ID terminée à TEMPS_COURANT"
                SI TEMPS_COURANT <= TACHE_ACTIVE_ID.ECHEANCE_ABSOLUE :
                    Afficher "Échéance respectée."
                SINON :
                    Afficher "Échéance manquée !"

                TACHE_ACTIVE_ID.INSTANCE = TACHE_ACTIVE_ID.INSTANCE + 1
                TACHE_ACTIVE_ID.PRET = FAUX
                Réinitialiser TACHE_ACTIVE_ID.TEMPS_EXECUTION_RESTANT = TACHE_ACTIVE_ID.TEMPS_EXECUTION
                Mettre à jour TACHE_ACTIVE_ID.TEMPS_ARRIVEE_ABSOLU pour la prochaine instance
                Mettre à jour TACHE_ACTIVE_ID.ECHEANCE_ABSOLUE pour la prochaine instance
                // Re-sélectionner la tâche la plus prioritaire immédiatement après la fin d'une tâche.
                // Cette logique est implicitement gérée par la sélection au début du prochain cycle.

        Incrémenter TEMPS_COURANT de 1
Fin TANT QUE

Fin Algorithme

Ce pseudo-code capture l'essence du comportement de l'ordonnanceur tel qu'il est implémenté en C. Il décrit le processus étape par étape, depuis l'initialisation des tâches jusqu'à la simulation de leur exécution sur l'hyperpériode.
Si vous aviez une autre attente pour "code algorithme", n'hésitez pas à préciser !
