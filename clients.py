import var

class Clientes():
    '''eventos clientes'''
    def validarDni(dni):
        '''codigo que controla la validez del dni'''

        try:
            tabla = 'TRWAGMYFPDXBNJZSQVHLCKE'
            dig_ext = 'XYZ'
            reemp_dig_ext ={'X':'0', 'Y':'1', 'Z':'2'}
            numeros = '0123456789'
            dni=dni.upper()
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                return len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control
                '''Va construyendo una lista, almacena el dato en ella si es un numero, al final comprueba que la lista creada tenga len=8'''
                '''Comprueba que la letra del dni corresponde con la de la tabla'''
            return False
        except:
            print('Error modulo validar DNI')
            return None


    def validoDni():
        try:
            dni = var.ui.editDni.text()
            if Clientes.validarDni(dni):
                var.ui.lblValidar.setStyleSheet('QLabel {color:green;}')
                var.ui.lblValidar.setText('V')
                var.ui.editDni.setText(dni.upper())
            else:
                var.ui.lblValidar.setStyleSheet('QLabel {color:red;}')
                var.ui.lblValidar.setText('X')
                var.ui.editDni.setText(dni.upper())
        except:
            print('Error modulo valido DNI')
            return None

    def selSexo():
        try:
            if var.ui.rbtFemenino.isChecked():
                print('Has elegido femenino')
            if var.ui.rbtMasculino.isChecked():
                print('Has elegido masculino')
        except Exception as error:
            print('Error: %s' % str(error))