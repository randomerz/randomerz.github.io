// IFTTT Slottt Machine by Jen Hamon
// jen@ifttt.com
// github.com/jhamon

var wordlist = [
    // 'Something something welcome to my website', // best length
    'Welcome to my website~',
    'Welcome to the boomo zone',
    'Hey there! Enjoy your stay :)',
    '┴┬┴┤･ω･)ﾉ├┬┴┬┴',
    'Please, take a seat',
    // 'I hope the weather\'s nice today!',
    'i am color-dot placing algorithm',
    // 'What are you listening to right now?',
    // 'What\'s the latest?',
    // 'Don\'t forget to drink water',
    'Hi! I\'m Daniel!',
    'Hey! I\'m boomo',
    'hello its me i am boomo',
    // 'You\'re watching the Boomo Channel',
    'Hi there! Try out my games!',
    // 'I\'m Daniel, but you can call me boomo',
    // 'Hello this is b- Daniel',
    'Wishlist Slider on Steam',
    // 'My grandkids will play Slider',

    // 'hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi ',
    // 'whatsssssssssss sssssssssssss up',
    // '!play christmas music',
    // 'おはようございます',
    // '방가방가',
    'Follow me @_boomo_',
    'Make a charisma roll',
    // 'Don\'t forget to join the boomo game jam',
    'Worthy opponent',
    // 'Head pats all around',
    // 'Average GDC enthusiast',
    // 'Chad\'s winrate is positive',
    // 'Ship it',
]

function buildSlotItem (text) {
    return $('<div>').addClass('slottt-machine-recipe__item')
                                        .text(text)
}

function buildSlotContents ($container, wordlist) {
    $items = wordlist.map(buildSlotItem);
    $container.append($items);
}

function popPushNItems ($container, n) {
    $children = $container.find('.slottt-machine-recipe__item');
    shuffle($children.slice(0, n)).insertAfter($children.last());

    if (n === $children.length) {
        popPushNItems($container, 1);
    }
}

function shuffle(array) {
    let currentIndex = array.length,  randomIndex;

    // While there remain elements to shuffle...
    while (currentIndex != 0) {

        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;

        // And swap it with the current element.
        [array[currentIndex], array[randomIndex]] = [
            array[randomIndex], array[currentIndex]];
    }

    return array;
}


// After the slide animation is complete, we want to pop some items off
// the front of the container and push them onto the end. This is
// so the animation can slide upward infinitely without adding
// inifinte div elements inside the container.
function rotateContents ($container, n) {
    setTimeout(function () {
        popPushNItems($container, n);
        $container.css({top: 0});
    }, 200);
}

function randomSlotttIndex(max) {
    var randIndex = (Math.random() * max) | 0;
    return (randIndex > 8) ? randIndex : randomSlotttIndex(max);
}



function animate() {
    var wordIndex = randomSlotttIndex(wordlist.length);
    $wordbox.animate({top: -wordIndex*121}, 1500, 'swing', function () {
        rotateContents($wordbox, wordIndex);
    });
}

$(function () {
    $wordbox = $('#wordbox .slottt-machine-recipe__items_container');
    shuffle(wordlist);
    if (wordlist.length > 20) {
        wordlist = wordlist.slice(0, 20);
    }
    buildSlotContents($wordbox, wordlist);
    // buildSlotContents($wordbox, wordlist);
    // buildSlotContents($wordbox, wordlist);
    // buildSlotContents($wordbox, wordlist);

    animate();
    // setInterval(animate, 2000);
});