# Guide de Contribution pour SafeZone AI

Nous sommes ravis que vous souhaitiez contribuer au projet SafeZone AI ! Vos contributions sont précieuses pour améliorer ce système de sécurité en temps réel.

Ce document décrit les lignes directrices pour contribuer au projet. En contribuant, vous acceptez de respecter ce guide.

## Comment Contribuer

### 1. Signaler des Bugs

Si vous trouvez un bug, veuillez ouvrir une [nouvelle issue](https://github.com/votre_utilisateur/SafeZone-AI/issues) sur GitHub. Avant de soumettre une nouvelle issue, veuillez vérifier si une issue similaire n'existe pas déjà.

Lorsque vous signalez un bug, veuillez inclure :

*   Une description claire et concise du bug.
*   Les étapes pour reproduire le bug.
*   Le comportement attendu et le comportement actuel.
*   Des captures d'écran ou des logs si possible.
*   Votre environnement (système d'exploitation, version de Python, dépendances).

### 2. Suggérer des Fonctionnalités

Nous sommes ouverts aux nouvelles idées et améliorations. Si vous avez une suggestion de fonctionnalité, veuillez ouvrir une [nouvelle issue](https://github.com/votre_utilisateur/SafeZone-AI/issues) sur GitHub.

Lorsque vous suggérez une fonctionnalité, veuillez inclure :

*   Une description claire et concise de la fonctionnalité proposée.
*   Pourquoi cette fonctionnalité serait utile pour le projet.
*   Des exemples d'utilisation si possible.

### 3. Soumettre des Pull Requests (PRs)

Pour les contributions de code, veuillez suivre les étapes suivantes :

1.  **Fork** le dépôt sur GitHub.
2.  **Clonez** votre fork localement :

    ```bash
    git clone https://github.com/votre_utilisateur/SafeZone-AI.git
    cd SafeZone-AI
    ```

3.  **Créez une nouvelle branche** pour vos modifications. Utilisez un nom descriptif (par exemple, `feature/nouvelle-fonctionnalite` ou `bugfix/corriger-erreur-x`) :

    ```bash
    git checkout -b feature/ma-nouvelle-fonctionnalite
    ```

4.  **Effectuez vos modifications.** Assurez-vous que votre code respecte les conventions de style existantes et qu'il est bien commenté.

5.  **Testez vos modifications.** Si vous ajoutez de nouvelles fonctionnalités, veuillez inclure des tests unitaires ou d'intégration si possible.

6.  **Commitez vos modifications** avec un message de commit clair et concis. Le message de commit doit décrire ce que la modification fait et pourquoi elle a été faite.

    ```bash
    git commit -m "feat: Ajouter une nouvelle fonctionnalité X"
    ```

    Types de commits recommandés (inspirés de Conventional Commits) :
    *   `feat`: Nouvelle fonctionnalité
    *   `fix`: Correction de bug
    *   `docs`: Changements de documentation
    *   `style`: Formatage, points-virgules manquants, etc. (pas de changement de code)
    *   `refactor`: Refactoring du code (pas de changement de fonctionnalité ni de bug)
    *   `test`: Ajout de tests manquants ou correction de tests existants
    *   `chore`: Mises à jour de la construction, des dépendances, etc.

7.  **Poussez vos modifications** vers votre fork sur GitHub :

    ```bash
    git push origin feature/ma-nouvelle-fonctionnalite
    ```

8.  **Ouvrez une Pull Request** depuis votre fork vers la branche `main` du dépôt original. Veuillez inclure :

    *   Une description détaillée de vos modifications.
    *   Les problèmes que votre PR résout (référencez les issues si applicable, par exemple `Closes #123`).
    *   Toute information supplémentaire pertinente (captures d'écran, résultats de tests).

### 4. Conventions de Code

*   **Python :** Suivez les conventions de style [PEP 8](https://www.python.org/dev/peps/pep-0008/).
*   **JavaScript/CSS/HTML :** Suivez les bonnes pratiques pour le développement web.
*   **Commentaires :** Commentez votre code de manière claire et concise, en expliquant les parties complexes ou non évidentes.

## Questions

Si vous avez des questions sur le processus de contribution, n'hésitez pas à ouvrir une issue ou à nous contacter.

Merci de votre intérêt et de votre contribution à SafeZone AI !


