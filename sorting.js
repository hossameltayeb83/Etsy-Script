let favCount=document.querySelectorAll('tbody td:nth-child(5)')
let mainTable= document.querySelector('table')

favCount.forEach(element => {
    
    if (element.innerHTML =='One favorite') {
        element.innerHTML = '1'
    } else if (element.innerHTML.includes('favorites'))  {
        
        element.innerHTML = element.innerHTML.substring(0, element.innerHTML.indexOf(' '));
    }else{
        element.innerHTML = '0'
    }
    
})


function sortTable(table,column,asc = true) {
    const dirModifier = asc ? 1:-1
    const tBody = table.tBodies[0]
    const rows = Array.from(tBody.querySelectorAll('tr'))
    const sortedRows = rows.sort((a,b)=>{
        const aColText = parseInt(a.querySelector(`td:nth-child(${column+1})`).textContent)
        const bColText = parseInt(b.querySelector(`td:nth-child(${column+1})`).textContent)    
        return aColText > bColText ? (1*dirModifier): (-1*dirModifier)
    })
    while (tBody.firstChild) {
        tBody.removeChild(tBody.firstChild)     
    }
    tBody.append(...sortedRows)

}
sortTable(mainTable,4,false)
