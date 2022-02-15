# Streamlit Custom Slider

An App where we load react components into streamlit. The data can be received and passed to these react components. We also integrated Flask API to make our requests allowing us to utilize machine learning models deloyed with Flask

#### Local Setup

```
# Requirments
Python 3.7.1rc2
node v16.14.0.
```

Install and run streamlit locally

```
$ python -m venv venv  # create venv
$ . venv/bin/activate   # activate venv
$ pip install -r requirements.txt # installing libraries
# App.py - Line:11, Replace url value from docker to local
# url = 'http://pythonapi:5000' with url = 'http://localhost:5000'
$ streamlit run app.py # Runs on port localhost:8501
```

Install & Run Python/Flask API:

```
# Flask API and its dependencies exists in pythonapi folder
$ cd pythonapi
$ python -m venv venv  # create venv
$ . venv/bin/activate   # activate venv
$ pip install -r requirements.txt
$ python app.y
```

Our React App

```
# The whole react app exists in frontend folder
cd streamlit_custom_slider/frontend
npm install
npm run start
```

#### Docker Setup

```
docker-compose build
docker-compose up
# The App is available at http://localhost:8501/
```

#### How to Information

```
streamlit_custom_slider/__init__.py
# This is where we have declard connection to react Components e.g st_custom_slider()
# one thing to note here is that You cannot connect with multiple react components

# This is the workaround, to load more than one components, create different route for each component on react side.

```

##### Python Side

```
streamlit_custom_slider/__init__.py

#Since we cannot load multiple components from one url, e.g url="http://localhost:3001/"
#Breaking components into multiple routes, e.g /dropdown, /slider.

_dropdown_func = components.declare_component(
    "custom_select",
    url="http://localhost:3001/dropdown",
)

#To connect with <CustomSlider /> on react side, Along with passing data this is how we do it,
_component_func = components.declare_component(
    "custom_slider",
    url="http://localhost:3001/slider",
)

# Arguments sent, accessible from props.args and result received from React component,
# Initial input is converted to an array and returned value
# (set through default and from React side is)extracted from the component
def st_custom_slider(label: str, min_value: int, max_value: int, value: int = 0, key=None) -> int:
    component_value = _component_func(label=label, minValue=min_value, maxValue=max_value, initialValue=[value], key=key, default=[value])
    return component_value[0]
```

##### React Side

```
// A routing Snipppets from index.tsx (React)
<Router>
         <Route path="/slider">
           <StyletronProvider value={engine}>
              <ThemeProvider theme={LightTheme}>
                <CustomSlider />
              </ThemeProvider>
            </StyletronProvider>
         </Route>

          <Route path="/dropdown">
            <CustomSelect />
          </Route>

          <Route path="/dropdown">
            <Component Value Here />
          </Route>
</Router>

//Two Important things, If you don't set the height, the component will not be visisble, taken from < CustomSelect />

useEffect(() => {
    Streamlit.setFrameHeight()
  })

//On Items like dropdown, to change component height on streamlit side on state toggle
 const onDropdownToggle = () => {
    Streamlit.setFrameHeight()
  }

//These components return value to streamlit, where they are loaded but how?
const onChange = (option) => {
    Streamlit.setComponentValue(option[0].value) //This sets the value of a component
    //Streamlit.setComponentValue(valueHere)
  }
```

##### Streamlit

```
app.py
#Importing Our Custom Component
from streamlit_custom_slider import st_custom_slider #from streamlit_custom_slider/__init__.py(Package)
#using them
input_features["age"] = st_custom_slider('Age', 18, 95, 50, key="age")


```
