const regionAllCheck = document.getElementById("region-all-check")
const regionAllCancel = document.getElementById("region-all-cancel")

regionAllCheck.addEventListener('click', () => {
  const checkboxes = document.getElementsByName('region')
  checkboxes.forEach((checkbox) => {
    checkbox.checked = true
  }) 
})

regionAllCancel.addEventListener('click', () => {
  const checkboxes = document.getElementsByName('region')
  checkboxes.forEach((checkbox) => {
    checkbox.checked = false
  }) 
})