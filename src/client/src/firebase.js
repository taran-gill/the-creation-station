import * as firebase from 'firebase/app';
import 'firebase/firestore';

const firebaseConfig = {
    apiKey: "AIzaSyCb_DjS8DyGH-uWYienhUrtMS5cifhTAZE",
    authDomain: "the-creation-station.firebaseapp.com",
    databaseURL: "https://the-creation-station.firebaseio.com",
    projectId: "the-creation-station",
    storageBucket: "the-creation-station.appspot.com",
    messagingSenderId: "225702327227",
    appId: "1:225702327227:web:9bbdb0f56367f01093ca9e"
};

const firebaseApp = firebase.initializeApp(firebaseConfig);

export { firebaseApp };
