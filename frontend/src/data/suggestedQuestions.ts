export interface SuggestedQuestion {
  en: string
  fr: string
}

export const suggestedQuestions: SuggestedQuestion[] = [
  // kMeet questions
  {
    en: 'How do I create a kMeet meeting?',
    fr: 'Comment créer une réunion kMeet ?',
  },
  {
    en: 'How can I share my screen during a kMeet call?',
    fr: 'Comment partager mon écran pendant un appel kMeet ?',
  },
  {
    en: 'What should I do if my audio is not working in kMeet?',
    fr: "Que faire si mon audio ne fonctionne pas dans kMeet ?",
  },
  {
    en: 'How do I create side rooms (breakout rooms) in kMeet?',
    fr: 'Comment créer des salles secondaires dans kMeet ?',
  },
  {
    en: 'How can I record a kMeet meeting?',
    fr: 'Comment enregistrer une réunion kMeet ?',
  },
  {
    en: 'How do I set a password for my kMeet meeting?',
    fr: 'Comment définir un mot de passe pour ma réunion kMeet ?',
  },
  {
    en: 'How can I livestream a kMeet meeting?',
    fr: 'Comment diffuser une réunion kMeet en direct ?',
  },
  {
    en: 'How do I enable automatic subtitles or transcription in kMeet?',
    fr: 'Comment activer les sous-titres automatiques dans kMeet ?',
  },
  {
    en: 'How do I join an existing kMeet meeting?',
    fr: 'Comment rejoindre une réunion kMeet existante ?',
  },
  {
    en: 'How can I use the whiteboard or drawing feature in kMeet?',
    fr: 'Comment utiliser le tableau blanc dans kMeet ?',
  },
  {
    en: 'How do I fix camera or video issues in kMeet?',
    fr: 'Comment résoudre les problèmes de caméra dans kMeet ?',
  },

  // kDrive questions
  {
    en: 'How do I install kDrive on Linux?',
    fr: 'Comment installer kDrive sur Linux ?',
  },
  {
    en: 'How can I share a file from kDrive?',
    fr: 'Comment partager un fichier depuis kDrive ?',
  },
  {
    en: 'What is a Drop Box in kDrive and how do I create one?',
    fr: "Qu'est-ce qu'une Drop Box dans kDrive et comment en créer une ?",
  },
  {
    en: 'How do I resolve sync conflicts in kDrive?',
    fr: 'Comment résoudre les conflits de synchronisation dans kDrive ?',
  },
  {
    en: 'How do I manage user rights in kDrive?',
    fr: 'Comment gérer les droits des utilisateurs dans kDrive ?',
  },
  {
    en: 'How can I access kDrive files locally without downloading them?',
    fr: 'Comment accéder aux fichiers kDrive localement sans les télécharger ?',
  },
  {
    en: 'How do I sync kDrive with my Synology NAS?',
    fr: 'Comment synchroniser kDrive avec mon NAS Synology ?',
  },
  {
    en: 'How do I sign a PDF document in kDrive?',
    fr: 'Comment signer un document PDF dans kDrive ?',
  },
  {
    en: 'How do I restore a file to a previous version in kDrive?',
    fr: 'Comment restaurer un fichier à une version précédente dans kDrive ?',
  },
  {
    en: 'How can I search for files within kDrive?',
    fr: 'Comment rechercher des fichiers dans kDrive ?',
  },
  {
    en: 'How do I view and manage my kDrive storage space?',
    fr: 'Comment voir et gérer mon espace de stockage kDrive ?',
  },
  {
    en: 'How can I scan documents with the kDrive mobile app?',
    fr: "Comment scanner des documents avec l'application mobile kDrive ?",
  },
  {
    en: 'How do I connect to kDrive via WebDAV?',
    fr: 'Comment se connecter à kDrive via WebDAV ?',
  },
  {
    en: 'What are the different folder types in kDrive?',
    fr: 'Quels sont les différents types de dossiers dans kDrive ?',
  },
  {
    en: 'How do I manage deleted files and the trash in kDrive?',
    fr: 'Comment gérer les fichiers supprimés et la corbeille dans kDrive ?',
  },
  {
    en: 'How do I restore my entire kDrive to a previous state?',
    fr: 'Comment restaurer mon kDrive entier à un état précédent ?',
  },

  // kChat questions
  {
    en: 'How do I create a channel in kChat?',
    fr: 'Comment créer un canal dans kChat ?',
  },
  {
    en: 'What slash commands are available in kChat?',
    fr: 'Quelles commandes slash sont disponibles dans kChat ?',
  },
  {
    en: 'How can I connect external applications to kChat?',
    fr: 'Comment connecter des applications externes à kChat ?',
  },
  {
    en: 'How do I translate a message in kChat?',
    fr: 'Comment traduire un message dans kChat ?',
  },
  {
    en: 'How can I invite external users to kChat?',
    fr: 'Comment inviter des utilisateurs externes à kChat ?',
  },
  {
    en: 'What is Euria and how do I use it in kChat?',
    fr: "Qu'est-ce qu'Euria et comment l'utiliser dans kChat ?",
  },
  {
    en: 'How do I set a reminder for a kChat message?',
    fr: 'Comment définir un rappel pour un message kChat ?',
  },
  {
    en: 'How do I send and manage voice messages in kChat?',
    fr: 'Comment envoyer et gérer les messages vocaux dans kChat ?',
  },
  {
    en: 'How do I use emoticons and GIFs in kChat?',
    fr: 'Comment utiliser les émoticônes et les GIFs dans kChat ?',
  },
  {
    en: 'How can I get a summary of a kChat discussion using Euria?',
    fr: "Comment obtenir un résumé d'une discussion kChat avec Euria ?",
  },
  {
    en: 'How do I customize kChat settings and display?',
    fr: "Comment personnaliser les paramètres et l'affichage de kChat ?",
  },
]

export function getRandomQuestions(
  lang: 'en' | 'fr',
  count: number = 5
): string[] {
  const shuffled = [...suggestedQuestions].sort(() => Math.random() - 0.5)
  return shuffled.slice(0, count).map((q) => q[lang])
}
