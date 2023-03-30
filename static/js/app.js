document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */


  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }


    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */


  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;
      this.dict = {};
      this.categories = [];

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      if (this.currentStep === 2) {
                if (getValuesFromForm() === false) {
                    this.currentStep = 1
                    alert("Wybierz kategorię.")
                    return;
                }
            }

      if (this.currentStep === 3) {
                if (bagsDonation() === "") {
                    this.currentStep = 2
                    alert("Podaj liczbę worków.")
                    return;
                }
            }
      if (this.currentStep === 4) {
                if (getValuesRadio() === false) {
                    this.currentStep = 3
                    alert("Wybierz instytucję.")
                    return;
                }
            }

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // TODO: get data from inputs and show them in summary



      if (this.currentStep == 3) {
        const markedCheckbox = document.querySelectorAll('input[type="checkbox"]:checked');

        for (const checkbox of markedCheckbox) {
          if (checkbox.checked)
            this.categories.push(checkbox.value);
        }

        const radio = document.querySelectorAll('input[type="radio"]');

        for (const element of radio) {
          const el_value = element.value.trim();

          if (this.categories.includes(el_value)) {
          element.parentElement.parentElement.style.display = 'block';

        }
        this.dict['categories']= element.value;
        }

      }
      if (this.currentStep == 5) {

        const marked_organization = document.querySelectorAll('input[type="radio"]:checked');

        for (const checked_organization of marked_organization) {
          if (checked_organization.checked)
            this.dict['organization'] = checked_organization.id;

        }
        const bags = document.querySelector('input[name="bags"]')
        this.dict['bags'] = bags.value
        const street = document.querySelector('input[name="address"]')
        this.dict['address'] = street.value
        const city = document.querySelector('input[name="city"]')
        this.dict['city'] = city.value
        const postcode = document.querySelector('input[name="postcode"]')
        this.dict['postcode'] = postcode.value
        const phone = document.querySelector('input[name="phone"]')
        this.dict['phone'] = phone.value
        const date = document.querySelector('input[name="date"]')
        this.dict['date'] = date.value
        const time = document.querySelector('input[name="time"]')
        this.dict['time'] = time.value
        this.dict['more_info'] = document.getElementById("more_info").value

        function change(old_value, new_value) {
          document.body.innerHTML = document.body.innerHTML.replace(old_value, new_value);
        }
        change(document.getElementById('summary_bags').innerText,'Ilość worków: ' + this.dict['bags']);
        change(document.getElementById('summary_institution').innerText, this.dict['organization']);
        change(document.getElementById('summary_street').innerText, this.dict['address']);
        change(document.getElementById('summary_city').innerText, this.dict['city']);
        change(document.getElementById('summary_postcode').innerText, this.dict['postcode']);
        change(document.getElementById('summary_phone').innerText, this.dict['phone']);
        change(document.getElementById('date').innerText, this.dict['date']);
        change(document.getElementById('hour').innerText, this.dict['time']);
        change(document.getElementById('alerts').innerText, this.dict['more_info']);



        const form = document.getElementById("form_data");

        let formBody = [];
        for (let property in this.dict) {
          let encodedKey = encodeURIComponent(property);
          let encodedValue = encodeURIComponent(this.dict[property]);
          formBody.push(encodedKey + "=" + encodedValue);
          }
          formBody = formBody.join("&");
          const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
          fetch('/donation/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
              'X-CSRFToken': csrftoken,

            },
            body: formBody
          })
      }

    }


    submit(e) {
      // e.preventDefault();

      this.currentStep++;
      this.updateForm();

      submitForm();

    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});

function getValuesFromForm() {
    const categoryArray = []
    const checkboxes = document.querySelectorAll('.form-group--checkbox > label > input[type="checkbox"]')
    checkboxes.forEach(function (el) {
        if (el.checked) {
            categoryArray.push(el.value)
        }
    })
    if (categoryArray.length < 1) {
        return false
    }
    return categoryArray
}

function bagsDonation() {
    const countBags = document.querySelector('input[name="bags"]').value
    return countBags
}

function getValuesRadio() {
  const institutionArray = [];
  const radio = document.querySelectorAll('.form-group--checkbox > label > input[type="radio"]');
  radio.forEach(function (el) {
    if (el.checked) {
        institutionArray.push(el.value)

      }
    if (institutionArray.length < 1) {
      return false
    }
    return institutionArray
  })}

