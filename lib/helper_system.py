import warnings

def suppress_warnings():
    warnings.filterwarnings('ignore')
    
    
__all__ = [
           
            'suppress_warnings',
          ]