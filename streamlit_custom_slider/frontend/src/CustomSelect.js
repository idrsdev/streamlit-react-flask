import React, { useEffect } from "react"
import Select from "react-dropdown-select"
import { Streamlit, withStreamlitConnection } from "streamlit-component-lib"

const CustomSelect = (props) => {
  const { label, options } = props.args

  const selectOptions =
    options &&
    options.map(function (option, index, array) {
      return { label: option, value: option }
    })
  const option = [selectOptions[0]]
  useEffect(() => {
    Streamlit.setFrameHeight()
  })

  const onChange = (option) => {
    Streamlit.setComponentValue(option[0].value)
  }
  const onDropdownToggle = () => {
    Streamlit.setFrameHeight()
  }

  return (
    <>
      <>{label}</>
      {options && (
        <Select
          onDropdownOpen={onDropdownToggle}
          onDropdownClose={onDropdownToggle}
          values={option}
          options={selectOptions}
          onChange={(values) => onChange(values)}
        />
      )}
    </>
  )
}

export default withStreamlitConnection(CustomSelect)
