function insertCharacterInto(characterId) {
    console.log(characterId, textInputToUse);
    var elem = document.getElementById(textInputToUse)
    var charToInsert = shadowRoot.getElementById(characterId).value
    var curPos = elem.selectionStart
    var text = elem.value;
    elem.value = text.slice(0, curPos) + charToInsert + text.slice(curPos);
    elem.focus()
    elem.selectionEnd = curPos + 1
}

function registerthis(inputId) {
    textInputToUse = inputId
    keyboardElem.hidden = false
}

function toUpper() {
    var elem = document.getElementById(textInputToUse)
    var curPos = elem.selectionStart;
    var curEnd = elem.selectionEnd;
    var text = elem.value;
    elem.value = text.slice(0, curPos) + text.slice(curPos, curEnd).toUpperCase() + text.slice(curEnd);
    elem.focus()
    elem.selectionEnd = curEnd
}


var shadowRoot;
var textInputToUse = null
var keyboardElem;

const textareaList = document.getElementsByTagName("textarea");
for(var i = 0; i < textareaList.length; i++){
    const elem = textareaList[i]
    console.log(elem.id)
    elem.addEventListener("focus", function() { registerthis(elem.id) })
    elem.setAttribute("spellcheck", "false")
}


class IndicTextInput extends HTMLElement {
    constructor() {
        super();

        this.attachShadow({mode: 'open'});
        shadowRoot = this.shadowRoot;
        const char_map = {
            0: {'a': 'disabled', 'ā': '_a', 'i': 'disabled', 'ī': '_i', 'u': 'disabled'},
            1: {'ū': '_u', 'r̥': '_r', 'e': 'disabled', 'ē': '_e', 'ai': 'disabled'},
            2: {'o': 'disabled', 'ō': '_o', 'ou': 'disabled', 'ṁ': '_m', 'ḥ': '_h'},
            3: {'k': 'disabled', 'kh': 'disabled', 'g': 'disabled', 'gh': 'disabled', 'ṅ': '_ng'},
            4: {'c': 'disabled', 'ch': 'disabled', 'j': 'disabled', 'jh': 'disabled', 'ñ': '_ny'},
            5: {'ṭ': '_t', 'ṭh': 'disabled', 'ḍ': '_d', 'ḍh': 'disabled', 'ṇ': '_N'},
            6: {'t': 'disabled', 'th': 'disabled', 'd': 'disabled', 'dh': 'disabled', 'n': 'disabled'},
            7: {'p': 'disabled', 'ph': 'disabled', 'b': 'disabled', 'bh': 'disabled', 'm': 'disabled'},
            8: {'ṟ': '_R', 'ḷ': '_l', 'ḻ': '_L', 'ś': '_sh', 'ṣ': '_Sh'},
            9: {'½': '_half', '¼': '_quarter'}
        }

        const table = document.createElement("table");
        for(var key in char_map) {
            const row = document.createElement("tr")
            table.appendChild(row);
            for(var elem in char_map[key]) {
                const cell = document.createElement("td")
                if(char_map[key][elem] == 'disabled') {
                    cell.innerHTML = "<input type='button' value='" + elem +"' disabled>";
                }
                else {
                    cell.innerHTML = "<input type='button' value='" + elem + "' id='" + char_map[key][elem] + "' onclick=\"insertCharacterInto(this.id)\">";
                }
                row.appendChild(cell);
            }
        }

        const row = document.createElement("tr")
        table.appendChild(row);
        const cell = document.createElement("td")
        cell.setAttribute("colspan", 5)
        cell.innerHTML = "<input type='button' value='Uppercase' id='_toupper' onclick='toUpper()'>"
        row.appendChild(cell);

        this.shadowRoot.append(table);
        <!--this.hidden = true-->
        keyboardElem = this
    }
}
customElements.define("indic-text-input", IndicTextInput)