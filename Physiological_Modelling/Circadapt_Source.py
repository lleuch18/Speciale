# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 10:35:27 2023

@author: Lasse
"""

############
# Set model_state
############
    def model_import(self, model_state, check_model_state=False) -> None:
        """
        Load model_state into CircAdapt object.

        Style and model_state version is automatically recognized.

        Parameters
        ----------
            model_state: dict
                model_state with data to set
            obj: str
                Object to set
        """
        # automatically recognize style of object model_state
        if len(model_state.keys()) == 3 \
                and 'CA' in model_state.keys() and 'Model' in model_state.keys() \
                and 'Solver' in model_state.keys():
            style = 'Custom'
        else:
            style = self._get_default_model_state_style()

        # here, style must be Custom or Empty, otherwise, raise error
        if style not in ["Custom", "Empty"]:
            raise ValueError('Unknown style')

        # Object is general style, so load according to general style
        if check_model_state:
            self._check_model_state(model_state)

        # TODO: build model according to object description
        self._set_model_state_model_parameters('Model', model_state['Model'])
        self._set_model_state_model_parameters('Model', model_state['Model'],
                                               field='state_variables')
        # self._set_model_state_model_parameters('Model', model_state['Model'],
        #                                        field='export_double_vectors')

        self._set_model_state_model_parameters('Solver', model_state['Solver'])

    def _check_model_state(self, model_state):
        """
        Check if model_state (param) is correct.

        Give warnings if versions do not match.
        """
        # check version
        if self.get('Version', str) < model_state['CA']['Version']:
            print('----------')
            print('- Warning: The stored P-dict origins from an other version'
                  ' than the used model.')
            print('-          Check the documentation whether this P-dict'
                  'is compatible.')

        # check model type
        if self.get('Model.type', str) != model_state['Model']['Type']:
            print('----------')
            print('- Warning: Model type is not the same. ')
            print('-          This might result in incomplete results.')
            print('-          Change the model name when building the model.')

        # check model name
        if self.get('Model.name', str) != model_state['Model']['Name']:
            print('----------')
            print('- Warning: Model type is not the same.')
            print('-          This might result in incomplete results.')
            print('-          Change the model name when building the model.')

        return True

# Set Parameters
    def _set_model_state_model_parameters1(self,
                                           level,
                                           components,
                                           field='parameters',
                                           field1='parameters_double',
                                           dtype=float,
                                           ):
        if field == "export_double_vectors":
            dtype = bool

        n_parameters = self.get(level + '.n_' + field1, int)
        if n_parameters > 0:
            # Set parameters
            for i in range(n_parameters):
                char_name = level + '.' + field1 + ':' + str(i)
                char_name = self.get(char_name, str)

                if char_name not in components[field]:
                    print('- Warning: Parameter ', char_name,
                          ' not in P-dict. Reference value is used. ')
                else:
                    if dtype == float:
                        succes = self._set_double(level+'.'+char_name,
                                                  components[field][char_name])
                    elif dtype == int:
                        succes = self._set_int(level+'.'+char_name,
                                               components[field][char_name])
                    elif dtype == bool:
                        succes = self._set_bool(level+'.'+char_name,
                                                components[field][char_name])
                    else:
                        succes = False

                    if not succes:
                        print('- Warning: parameter not set: ',
                              level + '.' + char_name)

    def _set_model_state_model_parameters(self,
                                          level,
                                          components,
                                          field='parameters',
                                          ):
        if field == "parameters":
            self._set_model_state_model_parameters1(
                level, components, field, field.lower()+"_double", dtype=float)
            self._set_model_state_model_parameters1(
                level, components, field, field.lower()+"_bool", dtype=bool)
            self._set_model_state_model_parameters1(
                level, components, field, field.lower()+"_int", dtype=int)
        else:
            self._set_model_state_model_parameters1(
                level, components, field, field.lower())

        if field == 'state_variables':
            self._set_state_variables(level, field, components)

        # solver does not have subcomponents, so return
        if level == 'Solver':
            return

        # Set subcomponents
        #n_subcomponents = int(self.get(level+'.Subcomponents', float))
        n_subcomponents = self.get(level+'.n_subcomponents', int)
        subcomponents_of_component = np.array(
            [sub_component['name']
             for sub_component in components['subcomponents']])
        if n_subcomponents > 0:
            for i in range(n_subcomponents):
                char_name = level + '.subcomponents:' + str(i)
                char_name = self.get(char_name, str)

                # warn if subcomponent is not in the model
                sub_component = subcomponents_of_component == char_name
                if np.sum(sub_component) == 0:
                    print('----------')
                    print('- Warning: Model subcomponent ', char_name,
                          ' not in P-dict. ')
                    print('-          Reference values are used. ')
                else:
                    self._set_model_state_model_parameters(
                        level + '.'
                        + components['subcomponents'][
                            np.argmax(sub_component)]['name'],
                        components['subcomponents'][np.argmax(sub_component)],
                        field=field,
                    )

    def _set_state_variables(self, level, field, components):
        n_parameters = self.get(level + '.n_' + field + '_vector', int)
        if n_parameters > 0:
            # Set parameters
            for i in range(n_parameters):
                char_name = level + '.' + field + '_vector:' + str(i + 1)
                char_name = self.get(char_name, str)

                if char_name not in components[field]:
                    print('- Warning: Parameter ', char_name,
                          ' not in P-dict. Reference value is used. ')
                else:
                    for i_vec in range(len(components[field][char_name])):
                        succes = self._set_double(
                            level + '.' + char_name + ':' + str(i_vec + 1),
                            components[field][char_name][i_vec],
                        )
                        if not succes:
                            print('- Warning: parameter not set: ',
                                  level + '.' + char_name + ':'
                                  + str(i_vec + 1))

############
# Get model_state
############
    def _get_default_model_state_style(self):
        """Get default style of the stored model state based on the name."""
        return 'General'

    def model_export(self, style: str = None) -> dict:
        """
        Return the stored model state.

        Parameters
        ----------
            style: str (optional)
                Style to follow. If not given, the default style from the model
                is used.

        Returns
        -------
            dict

        """
        if style is None:
            style = self._get_default_model_state_style()

        # if style is given, apply model_state style
        if style not in ["Custom", "General"]:
            raise ValueError('Unknown style')

        model = self._fill_model_state_model('Model')
        return {
            'CA': self._fill_model_state(),
            'Model': model,
            'Solver': self._fill_model_state_solver(),
        }

# CA
    def _fill_model_state(self):
        return {
            'Version': self.get('Version', str)
        }

# Fill Solver
    def _fill_model_state_solver(self):
        # Basics
        solver_type = self.get('Solver.type', str)
        # Parameters
        solver_parameters = self._fill_model_state_model_parameters('Solver')
        # State variables at last / next-first iteration
        # StateVariables = self.fill_model_state_model_parameters(
        #          'Solver', field='StateVariables')

        # Exported Features
        export_vectors = self._fill_model_state_model_double_vectors('Solver')
        return {'type': solver_type,
                'parameters': solver_parameters,
                'export_double_vectors': export_vectors}

# Fill model
    def _fill_model_state_model(self, level):
        # Basics
        level_name = self.get(level+'.name', str)
        level_type = self.get(level+'.type', str)
        # Subcomponents
        subcomponents = self._fill_model_state_model_subcomponents(level)
        # Parameters
        parameters = self._fill_model_state_model_parameters(level)
        # State variables at last / next-first iteration
        state_variables \
            = self._fill_model_state_model_parameters(level,
                                                      field='state_variables',
                                                      )
        state_variables \
            = self._fill_model_state_model_parameters_state_variable_vectors(
                level, state_variables)
        # Exported Features
        export_vectors = self._fill_model_state_model_double_vectors(level)
        return {'name': level_name,
                'type': level_type,
                'subcomponents': subcomponents,
                'parameters': parameters,
                'state_variables': state_variables,
                'export_double_vectors': export_vectors,
                }

# Get subcomponents
    def _fill_model_state_model_subcomponents(self, level):
        n_subcomponents = self.get(level+'.n_subcomponents', int)
        if n_subcomponents == 0:
            return []
        subcomponents = []
        for i in range(n_subcomponents):
            char_name = level+'.subcomponents:'+str(i)
            char_name = self.get(char_name, str)
            subcomponents.append(
                self._fill_model_state_model(level+'.'+char_name))
        return subcomponents

# Get Parameters
    def _fill_model_state_model_parameters(self,
                                           level,
                                           field='parameters',
                                           dtype=float,
                                           ):
        parameters = {}
        if field == "parameters":
            parameters = parameters | self._fill_model_state_model_parameters(
                level, field=field+'_double', dtype=float)
            parameters = parameters | self._fill_model_state_model_parameters(
                level, field=field+'_bool', dtype=bool)
            parameters = parameters | self._fill_model_state_model_parameters(
                level, field=field+'_int', dtype=int)
        else:
            n_parameters = self._get_int(level + '.n_' + field)
            if n_parameters == 0:
                return parameters
            for i in range(n_parameters):
                char_name = level+'.' + field + ':' + str(i)
                char_name = self.get(char_name, str)
                par = level + '.' + char_name
                parameters[char_name] = self.get(par, dtype)
        return parameters

    # Get Parameters
    def _fill_model_state_model_parameters_state_variable_vectors(
            self, level, state_variables):
        field = 'state_variables_vector'
        n_parameters = self.get(level + '.n_' + field, int)
        if n_parameters == 0:
            return state_variables
        for i in range(n_parameters):
            char_name = level + '.' + field + ':' + str(i + 1)
            par_name = self._get_str(char_name)
            vec = []
            len_par = int(self.get(level + '.' + par_name, float))
            for j in range(len_par):
                vec.append(self.get(level + '.' + par_name
                                    + ':' + str(j + 1), float))
            state_variables[par_name] = np.array(vec)
        return state_variables

# Get DoubleVectors
    def _fill_model_state_model_double_vectors(self, level,
                                               field='export_double_vectors'):
        n_parameters = self._get_int(level + '.n_' + field)
        if n_parameters == 0:
            return []
        parameters = {}
        # for i in range(n_parameters):
        #     char_name = level + '.' + field + ':' + str(i)
        #     char_name = self._get_str(char_name)
        #     if self._get_bool(level + '.' + char_name):
        #         parameters[char_name] = self._get_double_vector(level + '.'
        #                                                         + char_name)
        return parameters

    def save(self, filename: str, ext: str = None) -> None:
        """
        Save model to filename with extention.

        Parameters
        ----------
            filename: str
                Filename to save file to. Filename must have extention .npy or
                .mat
            ext: str (optional)
                Extention of the file. If not given, the last 3 letters of the
                filename is used to determine the save method.
        """
        if ext is None:
            ext = filename[-3:]

        if ext == 'npy':
            dataset = self.model_export(style='General')
            np.save(filename, dataset, allow_pickle=True)
            return
        if ext == 'mat':
            dataset = self.model_export()
            sio.savemat(filename, {'P': dataset})
            return
        raise ValueError('Extenstion not known')

    def load(self, filename: str) -> None:
        """
        Load a model dataset from a filename.

        Parameters
        ----------
            filename: str
                Path to file that will be loaded. The extension must be .npy or
                .mat.
        """
        if filename[-4:] == '.npy':
            dataset = np.load(filename, allow_pickle=True).item()
        elif filename[-4:] == '.mat':
            dataset = _check_keys(sio.loadmat(filename,
                                              struct_as_record=False,
                                              squeeze_me=True))['P']
        self.model_import(dataset)

    def is_success(self) -> bool:
        """
        Return false if vectors contain nan.

        Returns
        -------
            bool
        """
        return (self.get('Model.isCrashed', bool) and self.is_stable())

############
# Smart Components
############
    from .smart_components import add_smart_component
    from .smart_components_heart import build_heart, build_timings, \
        build_pfc
    from .smart_components_circulation import build_artven

    def __iter__(self):
        """
        Iterate over export dictionary.

        Designed to create a dictionary of the object using dict(self).

        Yields
        ------
            key: str
                key of dictionary
            data[key]: dict
                subdictionary of Pdict

        """
        data = self.model_export()
        for key, value in data.items():
            yield (key, value)

    def __setitem__(self, arg, val) -> bool:
        """
        Make self subscriptable.

        Parameters
        ----------
            arg: str or slice(None, None, None)
                If self[:], arg = slice(None, None, None) and set model
                import dictionary.
                If self['...'], return self.set(arg, val)
            val: dict or any
                Dictionary of the model or single value to set.
        """
        if arg == slice(None, None, None):
            return self.model_import(val)
        if isinstance(arg, str) and '.' not in arg:
            # TODO: implement partial dictionary
            raise ValueError('Currently, it is not possible to set partial '
                             'dictionaries. Please set the full dictionary '
                             'using self[:]. ')
        if isinstance(arg, str):
            return self.set(arg, val)
        raise ValueError('arg not known')

    def __getitem__(self, arg: any) -> any:
        """
        Make self object subscriptable.

        Parameters
        ----------
            arg: slice or str
                If self[:], arg = slice(None, None, None) and return model
                export dictionary.
                If self['...'], return self.get(arg)

        Returns
        -------
            model_export dictionary or self.get() type

        """
        if arg in self._components:
            return self._components[arg]
        if arg == slice(None, None, None):
            return self.model_export()
        if isinstance(arg, str) and '.' not in arg:
            # TODO: implement partial dictionary
            return self.model_export()[arg]
        if isinstance(arg, str):
            return self.get(arg)
        raise KeyError('Unknown key "' + str(arg) + '"')

    def __getstate__(self):
        """Get state manually, because ctypes can not be pickled."""
        state = self.__dict__.copy()
        state['data'] = self.model_export()
        del state['_model']
        return state

    def __setstate__(self, state):
        """Set state manually, because ctypes can not be pickled."""
        self.__init__(
            solver=state['_solver_name'],
            path_to_circadapt=state['path_to_circadapt'],
            )
        self.model_import(state['data'])

    def __repr__(self):
        """Object representation in string format."""
        return (
            '<' + self.__class__.__name__ + '>\n' +
            'CircAdapt object with keys:\n' +
            self.components.__repr__() + '\n' +
            '<\\' + self.__class__.__name__ + '>'
            )

    def copy(self):
        """Return a copy of itself."""
        raise NotImplementedError('Copy function not yet implemented for '
                                  'this instance.')