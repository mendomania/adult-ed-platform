const data = 'https://raw.githubusercontent.com/mendomania/adult-ed-platform/master/osr/static/osr/flow.json';

Vue.component('card', {
    template:`
<div>
  <div>
    <div class="row">
      <div class="columns small-12">
        <h6>{{ titleWithoutPlaceholders }}</h6>
      </div>
    </div>
    <div class="row">
      <div class="columns small-12">
        <h5 v-if="card.text[lang].tips.length == 0">
          {{ textWithoutPlaceholders }}
        </h5>
        <h5 v-else>
          {{ textWithoutPlaceholdersAndWithTooltips[0] }} 
          <div class="tooltip">
            {{ textWithoutPlaceholdersAndWithTooltips[1] }}
            <sup>i</sup>
            <span class="tooltiptext">{{ textWithoutPlaceholdersAndWithTooltips[3] }}</span>
          </div> 
          {{ textWithoutPlaceholdersAndWithTooltips[2] }}
        </h5>
      </div>
    </div>
    <div class="row">
      <div class="columns small-12">
        <p v-if="card.instructions[lang].length > 0">{{ card.instructions[lang] }}</p>
      </div>
    </div>

    <div v-if="card.type === 'CHECK'">
      <div v-for="(option,index) in optionsWithoutPlaceholdersAndWithTooltips">
        <div class="row">
          <div class="columns small-12">
            <input class="no-margin" name="currentCard" v-model="answers" :id="index" :value="option" type="checkbox"></input>
            <label class="no-margin" v-if="option.text[lang].tips.length == 0" :for="index">{{ option.text.updt }}</label>
            <label class="no-margin" v-else :for="index">{{ option.text.opts[0] }} <div class="tooltip">{{ option.text.opts[1] }}<sup>i</sup><span class="tooltiptext">{{ option.text.opts[3] }}</span></div> {{ option.text.opts[2] }}</label>        
          </div>
        </div>
      </div>
    </div>  

    <div v-if="card.type === 'RADIO'">
      <div v-for="(option,index) in optionsWithoutPlaceholdersAndWithTooltips">
        <div class="row">
          <div class="columns small-12">
            <input class="no-margin" name="currentCard" v-model="answers" :id="index" :value="option" type="radio"></input>
            <label class="no-margin" v-if="option.text[lang].tips.length == 0" :for="index">{{ option.text.updt }}</label>
            <label class="no-margin" v-else :for="index">{{ option.text.opts[0] }} <div class="tooltip">{{ option.text.opts[1] }}<sup>i</sup><span class="tooltiptext">{{ option.text.opts[3] }}</span></div> {{ option.text.opts[2] }}</label>
          </div>
        </div>            
      </div>
    </div>

    <div v-if="card.type === 'SELECT'">      
      <div class="row">
        <div class="columns small-12">         
          <select id="fieldOfWork" v-model="answers">  
            <option disabled value="">Please select one</option>
            <option v-for="(option,index) in card.options" :id="index" v-bind:value="option">{{ option.text[lang].main }}</option>
          </select>
        </div>
      </div>            
    </div>  

    <div v-if="card.type === 'INPUT_INT'">
      <div class="row">
        <div class="columns small-12 medium-12 large-12" style="align-items: center; display:flex !important;">
          <span style="padding-right:0.5rem;">{{ textWithoutPlaceholdersAndWithLabels[0] }}</span>
          <input id="enter" type="text" maxlength="2" v-model="answers" onkeypress='return event.charCode >= 48 && event.charCode <= 57' v-bind:style="{ width: card.options[0].width + 'px !important' }"/>
          <span style="padding-left:0.5rem;">{{ textWithoutPlaceholdersAndWithLabels[1] }}</span>
        </div>
      </div>
    </div> 

    <div v-if="card.type === 'INPUT_STR'">
      <div class="row">
        <div class="columns small-12 medium-12 large-12" style="align-items: center; display:flex !important;">
          <span style="padding-right:0.5rem;">{{ textWithoutPlaceholdersAndWithLabels[0] }}</span>
          <input id="enter" v-model="answers" type="text" v-bind:style="{ width: card.options[0].width + 'px !important' }"/>
          <span style="padding-left:0.5rem;">{{ textWithoutPlaceholdersAndWithLabels[1] }}</span>
        </div>
      </div>
    </div>    

    <br/>
    <div class="row">
      <div class="columns small-12">
        <div v-if="lang == 'en'">
          <button @click="backCard" class="quiz-button btn" v-if="card.id >= 1">&larr; Back</button>
          <button @click="nextCard" class="quiz-button btn">Next &rarr;</button>        
        </div>
        <div v-else>
          <button @click="backCard" class="quiz-button btn" v-if="card.id >= 1">&larr; Retour</button>
          <button @click="nextCard" class="quiz-button btn">Suivant &rarr;</button>        
        </div>
      </div>
    </div>
  </div>
</div>
`,
  data() {
    return {      
      // V-model for answers that were selected in current card
      answers: [],
    }
  },
  created() {},  
  updated() {    
    // Prints current state of the dictionary for debugging purposes
    console.log("$$$$$$$$$$ UPDATED $$$$$$$$$$");
    console.log(this.dico);
    console.log("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$");

    // The presence of flag will signal the end of the matchmaker
    if (this.dico['flag'] && ( this.dico['flag'] == 'T')) {
      this.submitForm();
    }   
  },     
  computed: {
    titleWithoutPlaceholders() {
      // Replace placeholders
      return this.fillInPlaceholders(this.card.title[this.lang]).toUpperCase();      
    },
    textWithoutPlaceholders() {
      // Replace placeholders
      return this.fillInPlaceholders(this.card.text[this.lang].main);
    }, 
    textWithoutPlaceholdersAndWithTooltips() {
      // Replace placeholders
      var text = this.fillInPlaceholders(this.card.text[this.lang].main);
      // Divide text in groups for tooltips
      return this.splitTextForTooltips(text, this.card.text[this.lang].tips[0].key, this.card.text[this.lang].tips[0].tip);
    },  
    textWithoutPlaceholdersAndWithLabels() {
      // Replace placeholders
      var text = this.fillInPlaceholders(this.card.options[0].text[this.lang].main);
      // Split text in labels that will precede and come after the text field
      return this.splitTextForLabels(text);
    },                               
    optionsWithoutPlaceholdersAndWithTooltips() {
      var options = Object.assign([], this.card.options);

      for (var i = 0; i < options.length; i++) {
        var text = options[i].text[this.lang].main;
        // Replace placeholders
        options[i].text.updt = this.fillInPlaceholders(options[i].text[this.lang].main);
        var tips = options[i].text[this.lang].tips;
        // Divide text
        if (tips.length > 0) {
          var arrVars = this.splitTextForTooltips(options[i].text[this.lang].main, tips[0].key, tips[0].tip);
          options[i].text["opts"] = [arrVars[0], arrVars[1], arrVars[2], arrVars[3]];
        }
      }

      return options;
    },         
  },     
  props: ['card', 'dico', 'lang'],
  methods: {
    /** 
    * Placeholders are variable names in between # symbols. If a string contains 
    * any, fill them in with values stored in the global dictionary. 
    * This of course presupposes that a card containing placeholders will always
    * be preceded by a card that will provide the dictionary with values needed 
    * to fill those in.
    */     
    fillInPlaceholders:function(text) {
      arrTags = text.match(/\#([^#]+)\#/g);
      if (arrTags) {
        for (var i = 0; i < arrTags.length; i++) {
          // Slicing removes the leading and trailing # symbols
          var key = arrTags[i].slice(1, -1);
          text = text.replace(arrTags[i], this.dico[key]);
        }
      }
      return text;
    },
    /** Texts are divided into 4 sections for display as tooltips */      
    splitTextForTooltips:function(text, key, tip) {
      arrDiv = [];
      numDiv = text.indexOf(key);
      // Substring that precedes the text with a tooltip
      arrDiv[0] = text.substr(0, numDiv);
      // Text that will have a superscript indicating a tooltip
      arrDiv[1] = key;
      // Substring that comes after the text with a tooltip
      arrDiv[2] = text.substr(numDiv + key.length, text.length - (numDiv + key.length));
      // Tooltip text
      arrDiv[3] = tip;
      return arrDiv;
    },
    /** 
    * Labels are strings that come before and after a text field. The position
    * of a text field in a string is indicated by the presence of a % symbol.
    */  
    splitTextForLabels:function(text) {
      arrDiv = [];
      numDiv = text.indexOf('%');
      // Label that precedes the text field
      arrDiv[0] = text.substr(0, numDiv - 1);
      // Label that comes after the text field
      arrDiv[1] = text.substr(numDiv + 2, text.length)
      return arrDiv;
    },    
    /** Moves back to the previous card */
    backCard:function() {  
      this.progressBarWidth = Math.round(this.progressBarWidth - (100/15)); 
      this.$emit('back');              
    },
    /** Moves on to the next card */
    nextCard:function() {
      switch (this.card.type) {
        case 'RADIO': {    
          // Assert some options were checked
          if (this.answers) {  
            this.progressBarWidth = Math.round(this.progressBarWidth + (100/15));
            var obj = { id: this.card.id, lang: this.lang, next: this.card.next, type: this.card.type, answers: this.answers };
            this.$emit('next', obj);
          }
          break;
        }
        case 'CHECK': { 
          // Assert some options were checked
          if (this.answers.length > 0) {
            this.progressBarWidth = Math.round(this.progressBarWidth + (100/15));
            var obj = { id: this.card.id, lang: this.lang, next: this.card.next, type: this.card.type, answers: this.answers };
            this.$emit('next', obj);
          }        
          break;
        }
        case 'SELECT': {
          if (this.answers) {
            this.progressBarWidth = Math.round(this.progressBarWidth + (100/15));
            var obj = { id: this.card.id, lang: this.lang, next: this.card.next, type: this.card.type, answers: this.answers };
            this.$emit('next', obj);
          }         
          break;
        }
        case 'INPUT_INT': {
          // Assert an answer was provided
          if (this.answers.length > 0) {      
            this.progressBarWidth = Math.round(this.progressBarWidth + (100/15));
            var input = { key: this.card.options[0].dico[0].key, val: this.answers };
            this.$emit('next', { id: this.card.id, lang: this.lang, next: this.card.next, type: this.card.type, answers: input });            
          }
          break;
        }
        case 'INPUT_STR': {
          if (this.answers.length > 0) {
            this.progressBarWidth = Math.round(this.progressBarWidth + (100/15));
            var input = { key: this.card.options[0].dico[0].key, val: this.answers };
            this.$emit('next', { id: this.card.id, lang: this.lang, next: this.card.next, type: this.card.type, answers: input });            
          }
          break;
        }        
      }

      // Reset
      this.answers = [];
    },
    /** 
    * Looks at the entries of the matchmaker dictionary that was updated 
    * throughout the whole quiz experience and then directs the user to a 
    * program results page.    
    */
    submitForm:function() {
      document.getElementById("jsform").submit();
    }
  }
});

const matchmaker = new Vue({
  el:'#matchmaker',
  data() {
    return {
      // Introductory stage of the quiz
      stageIntro: false,
      // Stage that cycles through all cards triggered by a user
      stageCards: false,
      // Array that stores all cards as defined in the JSON file
      cards: [],
      // Array that stores the IDs of all cards that have been visited
      visited: [],
      // ID of the card that is currently being visited
      currentCard: 0,
      // Dictionary that caches information collected from the answers
      // a user gives to the cards they go through
      dico: new Object(),
      // Language of the matchmaker
      lang: '',
      // Stack that stores the state of the matchmaker for every card 
      // that is visited so that the user can freely go back and forth
      // between cards in the matchmaker
      stack: []
    }
  },
  created() {
    this.lang = document.getElementById("lang").value;
    // Loads JSON file
    fetch(data)
    .then(res => res.json())
    .then(res => {
      this.cards = res.cards;
      this.stageIntro = true;
      this.stageCards = false;
    });   
  },
  methods: {
    /** 
    * Triggers the start of "stageCards" and pushes the initial state of 
    * the matchmaker to the stack that will be used when the user wants
    * to go back in the quiz.
    */    
    initQuiz() {
      // Signals the start of "stageCards"
      this.stageCards = true;
      this.stageIntro = false;
      this.dico = new Object();
      this.lang = document.getElementById("lang").value;
      // Pushes initial state of the matchmaker to stack  
      this.stack.push({ "stageIntro": false, "stageCards": true, "visited": [], 
        "currentCard": 0, "dico": new Object(), 
        "check": null, "radio": null, "input": null });  
    },
    /** Updates the language of the matchmaker */
    updtLang() {
      switch(document.getElementById("lang").value) {
        case 'en': {
          document.getElementById("lang").value = 'fr';
          break;
        }
        case 'fr': {
          document.getElementById("lang").value = 'en';
          break;
        }
      }
      this.lang = document.getElementById("lang").value;
    },

    /** 
    * Adds all entries that correspond to the answers a user selected in a  
    * given card to the matchmaker dictionary that will persist throughout
    * the whole quiz experience.
    */
    addCardValuesToDictionary(e) {
      switch (e.type) {
        case 'RADIO': {
          for (var i = 0; i < e.answers.dico.length; i++) {
            this.dico[e.answers.dico[i].key] = e.answers.dico[i].val[e.lang];
          }            
          break;
        }
        case 'CHECK': {
          for (var i = 0; i < e.answers.length; i++) {
            for (var j = 0; j < e.answers[i].dico.length; j++) {
              this.dico[e.answers[i].dico[j].key] = e.answers[i].dico[j].val[e.lang];
            }
          }           
          break;
        }
        case 'SELECT': {
          for (var i = 0; i < e.answers.dico.length; i++) {
            this.dico[e.answers.dico[i].key] = e.answers.dico[i].val[e.lang];
          }             
          break;
        }        
        case 'INPUT_INT': {
          this.dico[e.answers.key] = e.answers.val;
          break;
        }
        case 'INPUT_STR': {
          this.dico[e.answers.key] = e.answers.val;
          break;
        }             
      }       
    }, 

    // TODO:
    addExitValuesToDictionary(exit, lang) {
      for (var i = 0; i < exit.length; i++) {
        this.dico[exit[i].key] = exit[i].val[lang];
      }         
    },             

    // TODO:
    isConditionMet(key, val) {
      if (!(this.dico[key])) {
        return false;
      }

      if (val.charAt(0) == '<') {
        return parseInt(this.dico[key]) < parseInt(val.slice(1));
      } else if (val.charAt(0) == '>') {
        return parseInt(this.dico[key]) > parseInt(val.slice(1));
      } else {
        return (this.dico[key] == val);
      }
    },

    /** 
    * Determines what should be the next card to present to the user based 
    * on the "next" array of the current card, which contains all possible
    * paths and the conditions that should be met to trigger each of them.
    */    
    determineNextCard(next, lang) {
      // If there is only one possible path, then take it
      if (next.length == 1) {
        // Add 'exit' values to the matchmaker dictionary, if any
        if (next[0].exit) {
          this.addExitValuesToDictionary(next[0].exit, lang);
        } 
        return next[0];
      }

      // If there are several possible paths...
      else {        
        // Loop through all possible paths
        for (var i = 0; i < next.length; i++) {
          var bool = true;
          var curr = null;

          // If a path has no conditions, then take it
          if (next[i].conditions.length == 0) {
            
            // Add 'exit' values to the matchmaker dictionary, if any
            if (next[i].exit) {
              this.addExitValuesToDictionary(next[i].exit, lang);
            } 
            return next[i];
          }

          // Otherwise: Loop through conditions for the path
          for (var j = 0; j < next[i].conditions.length; j++) {
            // Keep going if a condition is met
            if (this.isConditionMet(next[i].conditions[j].key, next[i].conditions[j].val[lang])) {
              curr = next[i];
            }
            // Skip path if a condition is not met
            else {
              bool = false;
              break;
            }          
          }

          // If all conditions are met, take that path
          if (bool) {            
            // Add 'exit' values to the matchmaker dictionary, if any
            if (curr.exit) {
              this.addExitValuesToDictionary(curr.exit, lang);
            }
            return curr;
          }
        }
      }
    },

    /** 
    * Looks at the card equivalencies of a given card and determines if
    * one of them has been visited before. 
    */        
    wasVisitedBefore(cardNo) {
      if (this.visited.indexOf(cardNo) > 0) {
        return true;
      }      
      for (var x = 0; x < this.cards[cardNo].equivalencies.length; x++) {        
        if (this.visited.indexOf(this.cards[cardNo].equivalencies[x]) > 0) {
          return true;
        }
      }
      return false;
    },

    /** 
    * Pops the stack, discarding the value that corresponds to the current 
    * state of the matchmaker. Then sets the matchmaker to match its state
    * in the previous card, which is the value at the top of the stack.
    */   
    backCard() {
      var state = Object.assign({}, this.stack[this.stack.length - 1]);
      this.stack.pop();

      var state = Object.assign({}, this.stack[this.stack.length - 1]);
      this.stageIntro = state['stageIntro'];
      this.stageCards = state['stageCards'];
      this.visited = Object.assign([], state['visited']);
      this.dico = Object.assign({}, state['dico']);
      this.currentCard = state['currentCard'];    
    },

    /** 
    * Processes the answers a user gave to the current card and then moves
    * forward to the next card in the matchmaker.
    */         
    nextCard(e) {
      // Adds current card to array of visited cards
      this.visited.push(e.id);
      // Adds all values from current card to the matchmaker dictionary
      this.addCardValuesToDictionary(e);  


      // Resolves next card
      var me = this;
      var curr = null;
      var promise = new Promise(function(resolve, reject) {
        curr = me.determineNextCard(e.next, e.lang);
        me.currentCard = curr.id;
        while ((me.currentCard != -1) && (me.wasVisitedBefore(me.currentCard))) {
          curr = me.determineNextCard(me.cards[me.currentCard].next, e.lang);
          me.currentCard = curr.id;
        }    

        if ((me.currentCard == -1) || (!me.wasVisitedBefore(me.currentCard))) {
          resolve();
        }    
      });

      promise.then(function () {
        if (me.currentCard == -1) {        
          me.stageIntro = false;
          me.stageCards = false;
          // The presence of this flag will trigger a submit action in the updated()
          // method of the card component
          me.dico['flag'] = 'T';
          me.dico['lang'] = me.lang;
        }
      });

      // Pushes the current state of the matchmaker to the stack
      this.stack.push({ "stageIntro": this.stageIntro, "stageCards": this.stageCards, 
        "visited": Object.assign([], this.visited), "currentCard": this.currentCard, 
        "dico": Object.assign({}, this.dico), 
        "type": e.type,
        "answers": e.answers });
    }
  }
});
