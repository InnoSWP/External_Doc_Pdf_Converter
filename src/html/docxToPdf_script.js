function upload(selector, options = {}){
    const input = document.querySelector(selector)

    const open = document.createElement('button')
    open.classList.add('btn')
    open.textContent = 'Select files'

    if (options.multi){
        input.setAttribute('multiple', true)
    }

    if (options.accept && Array.isArray(options.accept)){
        input.setAttribute('accept', options.accept.join(','))
    }

    input.insertAdjacentElement('afterend', open)

    const triggerInput = () => input.click()

    const changeFiles = event => {
        if (!event.target.files.length){
            return
        }
    

        const files = Array.from(event.target.files)

        files.forEach(file => {
            console.log(file)

            const reader = new FileReader()
        })
    }



    open.addEventListener('click', triggerInput)
    input.addEventListener('change', changeFiles)
}


// app.js
upload('#file', {
    multi: true,
    accept: ['.docx', '.doc']
})